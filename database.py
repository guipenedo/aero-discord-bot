from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Date

import config

engine = create_engine(config.POSTGRE_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=False)
    access_token = Column('access_token', String)
    refresh_token = Column('refresh_token', String)
    token_expires = Column('token_expires', Integer)

    def __init__(self, user_id, access_token, refresh_token, token_expires):
        self.user_id = user_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires = token_expires


class Cadeira(Base):
    __tablename__ = "cadeiras"

    cadeira_id = Column(Integer, primary_key=True, autoincrement=False)
    acronym = Column('acronym', String)
    name = Column('name', String)
    academic_term = Column('academic_term', String)
    last_updated = Column("last_updated", Date)
    feed_link = Column('feed_link', String)
    channel_id = Column('channel_id', Integer)
    role_id = Column('role_id', Integer)

    def __init__(self, cadeira_id, acronym, name, academic_term, last_updated, feed_link, channel_id, role_id):
        self.cadeira_id = cadeira_id
        self.acronym = acronym
        self.name = name
        self.academic_term = academic_term
        self.last_updated = last_updated
        self.feed_link = feed_link
        self.channel_id = channel_id
        self.role_id = role_id
