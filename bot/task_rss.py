from threading import Thread
import config
import time
from database import Session, engine, Base, Cadeira
import feedparser
import datetime
import bot

Base.metadata.create_all(engine)
session = Session()


class TaskRss(Thread):
    def run(self):
        while True:
            for cadeira in session.query(Cadeira).all():
                # TODO: fetch new rss articles and send to bot
                feed = feedparser.parse(cadeira.feed_link)
                for e in feed.entries:
                    if cadeira.last_updated is None or cadeira.last_updated < datetime.datetime(*(e.updated_parsed[0:6])):
                        channel = bot.bot.get_channel(cadeira.channel_id)

                continue
            time.sleep(config.FEED_UPDATE_INTERVAL)
