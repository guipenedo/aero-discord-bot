from database import session, Cadeira, User
from fenix import fenix_client
from .utils import not_aero, criar_cadeira
import config

from discord.ext import tasks, commands


class TaskNewUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("starting")
        self.newusers.start()

    def cog_unload(self):
        self.newusers.cancel()

    @tasks.loop(seconds=10)
    async def newusers(self):
        users = session.query(User).filter(User.initialized == False).all()
        guild = self.bot.get_guild(config.BOT_GUILD)
        for user in users:
            duser = guild.get_member(user.user_id)
            if duser is None:
                print("deleting user")
                #session.delete(user)
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
            for cadeira in cadeiras["enrolments"]:
                cadeira_id = int(cadeira["id"])
                db_cadeira = session.query(Cadeira).get(cadeira_id)
                if db_cadeira is None:
                    db_cadeira = await criar_cadeira(cadeira_id, self.bot)
                role = guild.get_role(db_cadeira.role_id)
                channel = guild.get_channel(db_cadeira.channel_id)
                # in case either the channel or the role was deleted
                if channel is None or role is None:
                    session.delete(db_cadeira)
                    db_cadeira = await criar_cadeira(cadeira_id, self.bot)
                    role = guild.get_role(db_cadeira.role_id)
                nomes_cadeiras.append(db_cadeira.name)
                new_roles.append(role)
            if new_roles:
                await duser.add_roles(*new_roles)

            user.initialized = True
            await duser.send("Auth concluída! \nFoste adicionado às seguintes cadeiras: ***"
                             + ', '.join(nomes_cadeiras) + "***")
        if len(users):
            session.commit()

    @newusers.before_loop
    async def before_newusers(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(TaskNewUser(bot))
