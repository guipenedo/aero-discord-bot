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

    @tasks.loop(seconds=500)
    async def newusers(self):
        users = session.query(User).filter(User.initialized == False).all()
        guild = self.bot.get_guild(config.BOT_GUILD)
        for user in users:
            duser = guild.get_member(user.user_id)
            if duser is None:
                print("deleting user")
                #session.delete(user)
                continue
            # TODO: ask for new auth if access token no longer valid
            person = fenix_client.get_person(user)
            if not_aero(person):
                await duser.send(
                    "Neste momento, os registos estão limitados aos estudantes de aeroespacial. Sorry ;(")
                #session.delete(user)
                continue
            # curriculum = fenix_client.get_person_curriculum(user)
            cadeiras = fenix_client.get_person_courses(user)
            new_roles = []
            for cadeira in cadeiras["enrolments"]:
                cadeira_id = int(cadeira["id"])
                db_cadeira = session.query(Cadeira).get(cadeira_id)
                if db_cadeira is None:
                    print("criando cadeira")
                    db_cadeira = await criar_cadeira(cadeira_id, self.bot)
                role = guild.get_role(db_cadeira.role_id)
                new_roles.append(role)
            if new_roles:
                await duser.add_roles(new_roles)

            # user.initialized = True
            await duser.send("Auth concluída!")
        if len(users):
            session.commit()

    @newusers.before_loop
    async def before_newusers(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(TaskNewUser(bot))
