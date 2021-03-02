from sqlalchemy import Column, String, Integer, BigInteger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import DateTime, Boolean
from contextlib import contextmanager

import config

engine = create_engine(config.DATABASE_URL)
Session = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(engine)
    with session_scope() as session:
        session.commit()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=False)
    access_token = Column(String)
    refresh_token = Column(String)
    token_expires = Column(Integer)
    initialized = Column(Boolean, default=False)
    new_semester = Column(Boolean, default=True)

    def __init__(self, user_id, access_token, refresh_token, token_expires):
        self.user_id = user_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires = token_expires


class Cadeira(Base):
    __tablename__ = "cadeiras"

    cadeira_id = Column(BigInteger, primary_key=True, autoincrement=False)
    acronym = Column(String)
    name = Column(String)
    academic_term = Column(String)
    last_updated = Column(DateTime)
    feed_link = Column(String)
    channel_id = Column(BigInteger)
    role_id = Column(BigInteger)

    def __init__(self, cadeira_id, acronym, name, academic_term, feed_link, channel_id, role_id):
        self.cadeira_id = cadeira_id
        self.acronym = acronym
        self.name = name
        self.academic_term = academic_term
        self.feed_link = feed_link
        self.channel_id = channel_id
        self.role_id = role_id
