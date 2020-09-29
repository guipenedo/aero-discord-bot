from threading import Thread
import config
import time
from database import Session, engine, Base, User

Base.metadata.create_all(engine)
session = Session()


class TaskNewUser(Thread):
    def run(self):
        while True:
            for User in session.query(User).get():
                # TODO: fetch new rss articles and send to bot
                continue
            time.sleep(config.FEED_UPDATE_INTERVAL)
