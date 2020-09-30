import config
#from database import session, Cadeira
import feedparser
import datetime

from discord.ext import tasks, commands


class TaskRss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rss.start()

    def cog_unload(self):
        self.rss.cancel()

    @tasks.loop(seconds=config.FEED_UPDATE_INTERVAL)
    async def rss(self):
        pass
        # for cadeira in session.query(Cadeira).all():
        #     # TODO: fetch new rss articles and send to bot
        #     feed = feedparser.parse(cadeira.feed_link)
        #     for e in feed.entries:
        #         if cadeira.last_updated is None or cadeira.last_updated < datetime.datetime(
        #                 *(e.updated_parsed[0:6])):
        #             channel = self.bot.get_channel(cadeira.channel_id)

    @rss.before_loop
    async def before_rss(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(TaskRss(bot))
