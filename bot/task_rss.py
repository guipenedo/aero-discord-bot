import config
from database import session, Cadeira
import feedparser
import datetime
import time
from htmllaundry import strip_markup

from discord.ext import tasks, commands
from .utils import format_msg, timezone


class TaskRss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rss.start()

    def cog_unload(self):
        self.rss.cancel()

    @tasks.loop(seconds=config.FEED_UPDATE_INTERVAL)
    async def rss(self):
        for cadeira in session.query(Cadeira).all():
            feed = feedparser.parse(cadeira.feed_link)
            feed.entries.sort(key=lambda x: x.updated_parsed)
            for e in feed.entries:
                postdate = datetime.datetime(*(e.updated_parsed[0:6]))
                if cadeira.last_updated is None or cadeira.last_updated < postdate:
                    channel = self.bot.get_channel(cadeira.channel_id)
                    cadeira.last_updated = postdate
                    message = format_msg(config.MSG_FEED, {
                        "course_acronym": cadeira.acronym,
                        "course_name": cadeira.name,
                        "title": e.title,
                        "date": time.strftime('%d/%m/%Y %H:%M', timezone(e.updated_parsed)),
                        "author": e.author,
                        "link": e.link
                    })
                    if "{description}" in message:
                        description = strip_markup(e.description.replace("<br />", "\n").replace("<p>", "\n"))
                        if len(message) + len(e.description) - len('{description}') > 2000:
                            description = description[:2000 - len(message) + len('{description}') - 3] + '...'
                        message = message.replace("{description}", description)
                    await channel.send(message)
        session.commit()

    @rss.before_loop
    async def before_rss(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(TaskRss(bot))
