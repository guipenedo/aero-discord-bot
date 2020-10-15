import config
from database import session, User
from discord.ext import tasks, commands
from .utils import format_msg, get_auth_url


class TaskAuthLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notauthusers.start()

    def cog_unload(self):
        self.notauthusers.cancel()

    async def notify_auth_users(self):
        guild = self.bot.get_guild(config.BOT_GUILD)

        members_discord = guild.getmembers()
        members_db = session.query(User.user_id).all()

        for member in members_discord:
            if member.id not in members_db:
                try:
                    url = get_auth_url(member)
                    await member.send(format_msg(config.MSG_REJOIN, {'name': member.display_name, 'url': url}))
                except:
                    pass

    # this task notifies users that are not authenticated yet
    @tasks.loop(hours=config.NOTIFY_USER_INTERVAL)
    async def notauthusers(self):
        await self.notify_auth_users()

    @notauthusers.before_loop
    async def before_notauthusers(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(TaskAuthLink(bot))
