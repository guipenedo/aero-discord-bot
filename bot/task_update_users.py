from database import session, Cadeira, User
from fenix import fenix_client
from .utils import not_aero, criar_cadeira
import config

from discord.ext import tasks, commands


class TaskUpdateUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.updateusers.start()

    def cog_unload(self):
        self.updateusers.cancel()

    @tasks.loop(seconds=config.UPDATE_USER_INTERVAL)
    async def updateusers(self):
        # Get initialized users and guild
        users = session.query(User).filter(User.initialized == True).all()
        guild = self.bot.get_guild(config.BOT_GUILD)

        # Loop through users
        for user in users:
            # Delete user from db if it is not in the guild
            duser = guild.get_member(user.user_id)
            if duser is None:
                print("deleting user")
                #session.delete(user)
                continue
            
            # Delete user from db if it is not from aero
            person = fenix_client.get_person(user)
            if not_aero(person):
                await duser.send(
                    "Neste momento, os registos estão limitados aos estudantes de aeroespacial. Sorry ;(")
                print("deleting user")
                #session.delete(user)
                continue

            # Get user current courses
            new_channels = []
            new_roles = []

            # Add person to year channel
            curriculo = fenix_client.get_person_curriculum(user)
            ano = curriculo["currentYear"]
            matriculas = get_number_enrollments(person)
            #INCOMPLETE

            # Loop through courses
            cadeiras = fenix_client.get_person_courses(user)
            for cadeira in cadeiras["enrolments"]:
                # Create channel for course if it doesn't exist
                cadeira_id = int(cadeira["id"])
                db_cadeira = session.query(Cadeira).get(cadeira_id)
                if db_cadeira is None:
                    db_cadeira = await criar_cadeira(cadeira_id, self.bot)

                # Create role if it doesn't exist
                role = guild.get_role(db_cadeira.role_id)
                channel = guild.get_channel(db_cadeira.channel_id)

                # In case either the channel or the role were deleted
                if channel is None or role is None:
                    session.delete(db_cadeira)
                    db_cadeira = await criar_cadeira(cadeira_id, self.bot)
                    role = guild.get_role(db_cadeira.role_id)

                # Cadeiras e roles
                new_channels.append(db_cadeira.name)
                new_roles.append(role)

            # Add roles to user
            if new_roles:
                await duser.add_roles(*new_roles)

            user.initialized = True
            await duser.send("Auth concluída! \nFoste adicionado às seguintes cadeiras: ***"
                             + ', '.join(new_channels) + "***")
        if len(users):
            session.commit()

    @updateusers.before_loop
    async def before_updateusers(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(TaskUpdateUser(bot))
