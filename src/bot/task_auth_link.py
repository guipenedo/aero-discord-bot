import config
from discord.ext import tasks, commands
from .utils import format_msg, get_auth_url, get_or_create_role


class TaskAuthLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notauthusers.start()

    def cog_unload(self):
        self.notauthusers.cancel()

    async def notify_auth_users(self):
        guild = self.bot.get_guild(config.BOT_GUILD)
        members_discord = guild.members

        auth_role = await get_or_create_role(guild, config.ROLE_AUTH_NAME)

        for member in members_discord:
            if auth_role not in member.roles:
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
