from database import session, Cadeira, User
from fenix import fenix_client
from .utils import not_aero, criar_cadeira, get_first_enrollment, get_or_create_year_role
import config

from discord.ext import tasks, commands


class TaskNewUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.newusers.start()
        self.existingusers.start()

    def cog_unload(self):
        self.newusers.cancel()
        self.existingusers.cancel()

    async def update_users(self, initialized=False):
        users = session.query(User).filter(User.initialized == initialized).all()
        guild = self.bot.get_guild(config.BOT_GUILD)

        all_cadeiras_roles = []
        # if we are updating existing users, remove all cadeiras first
        if users and initialized:
            all_cadeiras_roles = [guild.get_role(x.role_id) for x in session.query(Cadeira).all()]

        # Loop through users
        for user in users:
            # Delete user from db if not in the guild
            duser = guild.get_member(user.user_id)
            if duser is None:
                session.delete(user)
                continue
            person = fenix_client.get_person(user)
            if not_aero(person):
                await duser.send(
                    "Neste momento, os registos estão limitados aos estudantes de aeroespacial. Sorry ;(")
                session.delete(user)
                continue

            cadeiras = fenix_client.get_person_courses(user)
            nomes_cadeiras = []
            new_roles = []
            user_roles = duser.roles

            # first timer. add to the correct year discussion channel
            if initialized is False:
                first_enroll = get_first_enrollment(person)
                if first_enroll:
                    year_role = await get_or_create_year_role(first_enroll, self.bot)
                    await duser.add_roles(year_role)
                    await duser.send("Foste adicionado ao channel de discussão dos caloiros de ***"
                                     + first_enroll + "***")

            # Loop through courses
            for cadeira in cadeiras["enrolments"]:
                cadeira_id = int(cadeira["id"])
                db_cadeira = session.query(Cadeira).get(cadeira_id)
                # Create channel for course if it doesn't exist
                if db_cadeira is None:
                    db_cadeira = await criar_cadeira(cadeira_id, self.bot)

                # Get (or create) role for this course
                role = guild.get_role(db_cadeira.role_id)
                channel = guild.get_channel(db_cadeira.channel_id)

                # in case either the channel or the role was deleted
                if channel is None or role is None:
                    session.delete(db_cadeira)
                    db_cadeira = await criar_cadeira(cadeira_id, self.bot)
                    role = guild.get_role(db_cadeira.role_id)
                if role not in user_roles:
                    nomes_cadeiras.append(db_cadeira.name)
                    new_roles.append(role)
                else:
                    user_roles.remove(role)
            if new_roles:
                await duser.add_roles(*new_roles)

            # look for roles from old cadeiras
            remove_roles = []
            for role in user_roles:
                # check if this is a course role and not some random role
                if role in all_cadeiras_roles:
                    remove_roles.append(role)
            # remove them
            if remove_roles:
                await duser.remove_roles(*remove_roles)

            user.initialized = True
            await duser.send("Foste adicionado às seguintes cadeiras: ***"
                             + ', '.join(nomes_cadeiras) + "***")
            if initialized is False:
                await duser.send("Auth concluída!")
        if users:
            session.commit()

    # this task adds new users
    @tasks.loop(seconds=config.NEW_USER_INTERVAL)
    async def newusers(self):
        await self.update_users()

    @newusers.before_loop
    async def before_newusers(self):
        await self.bot.wait_until_ready()

    # this task updates existing users' info
    @tasks.loop(minutes=config.UPDATE_USER_INTERVAL)
    async def existingusers(self):
        await self.update_users(True)

    @existingusers.before_loop
    async def before_existingusers(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(TaskNewUser(bot))
