import discord
from discord.ext import tasks, commands

import config
from database import session_scope, User
from fenix import fenix_client
from .utils import process_enrollments, get_auth_url


class TaskUserNewSemester(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.usersnewsemester.start()

    def cog_unload(self):
        self.usersnewsemester.cancel()

    async def update_users(self):
        with session_scope() as session:
            user = session.query(User).filter(User.initialized==True, User.new_semester==False).first()

            if not user:
                return

            guild = self.bot.get_guild(config.BOT_GUILD)

            # Delete user from db if not in the guild
            duser = guild.get_member(user.user_id)
            if duser is None:
                session.delete(user)
                return
            person = fenix_client.get_person(user)
            if "error" in person and "accessTokenInvalid" in person["error"]:
                # fenix api token error: resend link
                try:
                    await duser.send("Não foi possível atualizar automaticamente a tua lista de cadeiras. Por favor volta a autenticar-te clicando em:\n"
                                     + get_auth_url(duser))
                except discord.errors.Forbidden:
                    pass
                user.new_semester = True
                return

            cadeiras = fenix_client.get_person_courses(user)

            # Loop through courses
            await process_enrollments(cadeiras, duser, self.bot)
            print("Updated", user.user_id, "for the new semester.")
            user.new_semester = True

    # this task adds new users
    @tasks.loop(seconds=config.UPDATE_USER_INTERVAL)
    async def usersnewsemester(self):
        await self.update_users()

    @usersnewsemester.before_loop
    async def before_usersnewsemester(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(TaskUserNewSemester(bot))
