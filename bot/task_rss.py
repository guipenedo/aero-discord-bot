from threading import Thread
import config
import time
from database import Session, engine, Base, Cadeira
import feedparser

Base.metadata.create_all(engine)
session = Session()


class TaskRss(Thread):
    def run(self):
        while True:
            for cadeira in session.query(Cadeira).all():
                # TODO: fetch new rss articles and send to bot
                continue
            time.sleep(config.FEED_UPDATE_INTERVAL)
