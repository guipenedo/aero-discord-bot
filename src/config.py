import os
from dotenv import load_dotenv
load_dotenv(".env")


def clean_msg(msg):
    return msg.replace('\\n', '\n')

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_GUILD = int(os.environ.get("BOT_GUILD"))
BOT_CMD_PREFIX = os.environ.get("BOT_CMD_PREFIX")

FENIX_BASE_URL = os.environ.get("FENIX_BASE_URL")
FENIX_DEGREES = [int(x) for x in os.environ.get("FENIX_DEGREES").split(",")]
FENIX_CLIENT_ID = os.environ.get("FENIX_CLIENT_ID")
FENIX_CLIENT_SECRET = os.environ.get("FENIX_CLIENT_SECRET")
FENIX_REDIRECT_URI = os.environ.get("FENIX_REDIRECT_URI")

DATABASE_URL = os.environ.get("DATABASE_URL")

NEW_USER_INTERVAL = int(os.environ.get("NEW_USER_INTERVAL"))
NOTIFY_USER_INTERVAL = int(os.environ.get("NOTIFY_USER_INTERVAL"))
UPDATE_USER_INTERVAL = int(os.environ.get("UPDATE_USER_INTERVAL"))
FEED_UPDATE_INTERVAL = int(os.environ.get("FEED_UPDATE_INTERVAL"))

FEEDS_CATEGORY_NAME = os.environ.get("FEEDS_CATEGORY_NAME").lower()
COURSES_DISC_CATEGORY_NAME = os.environ.get("COURSES_DISC_CATEGORY_NAME").lower()
YEARS_DISC_CATEGORY_NAME = os.environ.get("YEARS_DISC_CATEGORY_NAME").lower()

WEB_ERROR = clean_msg(os.environ.get("WEB_ERROR"))
WEB_SUCCESS = clean_msg(os.environ.get("WEB_SUCCESS"))

TIMEZONE = os.environ.get("TIMEZONE")

MSG_JOIN = clean_msg(os.environ.get("MSG_JOIN"))
MSG_REJOIN = clean_msg(os.environ.get("MSG_REJOIN"))
MSG_FEED = clean_msg(os.environ.get("MSG_FEED"))
MSG_AERO_ONLY = clean_msg(os.environ.get("MSG_AERO_ONLY"))
MSG_ADDED_CHANNEL_COURSES = clean_msg(os.environ.get("MSG_ADDED_CHANNEL_COURSES"))
MSG_ADDED_CHANNEL_YEAR = clean_msg(os.environ.get("MSG_ADDED_CHANNEL_YEAR"))

BOT_CMD_ERROR = clean_msg(os.environ.get("BOT_CMD_ERROR"))
BOT_AUTH_SUCCESS = clean_msg(os.environ.get("BOT_AUTH_SUCCESS"))

ROLE_AUTH_NAME = os.environ.get("ROLE_AUTH_NAME")
