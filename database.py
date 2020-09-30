from sqlalchemy import Column, String, Integer, BigInteger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Date, Boolean

import config

engine = create_engine(config.DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.create_all(engine)
session = Session()


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=False)
    access_token = Column(String)
    refresh_token = Column(String)
    token_expires = Column(Integer)
    initialized = Column(Boolean, default=False)

    def __init__(self, user_id, access_token, refresh_token, token_expires):
        self.user_id = user_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires = token_expires


class Cadeira(Base):
    __tablename__ = "cadeiras"

    cadeira_id = Column(Integer, primary_key=True, autoincrement=False)
    acronym = Column(String)
    name = Column(String)
    academic_term = Column(String)
    last_updated = Column(Date)
    feed_link = Column(String)
    channel_id = Column(Integer)
    role_id = Column(Integer)

    def __init__(self, cadeira_id, acronym, name, academic_term, feed_link, channel_id, role_id):
        self.cadeira_id = cadeira_id
        self.acronym = acronym
        self.name = name
        self.academic_term = academic_term
        self.feed_link = feed_link
        self.channel_id = channel_id
        self.role_id = role_id
