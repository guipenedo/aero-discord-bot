import os
from dotenv import load_dotenv
load_dotenv(".env")

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_GUILD = int(os.environ.get("BOT_GUILD"))
BOT_CMD_PREFIX = os.environ.get("BOT_CMD_PREFIX")

FENIX_BASE_URL = os.environ.get("FENIX_BASE_URL")
FENIX_DEGREE = os.environ.get("FENIX_DEGREE")
FENIX_CLIENT_ID = os.environ.get("FENIX_CLIENT_ID")
FENIX_CLIENT_SECRET = os.environ.get("FENIX_CLIENT_SECRET")
FENIX_REDIRECT_URI = os.environ.get("FENIX_REDIRECT_URI")

DATABASE_URL = os.environ.get("DATABASE_URL")

FEED_UPDATE_INTERVAL = int(os.environ.get("FEED_UPDATE_INTERVAL"))

MSG_JOIN = os.environ.get("MSG_JOIN").replace('\\n', '\n')
