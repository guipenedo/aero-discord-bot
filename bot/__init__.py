import fenixedu
from discord.ext import commands

from database import Session, engine, Base
import config

Base.metadata.create_all(engine)
session = Session()

fen_config = fenixedu.FenixEduConfiguration(config.FENIX_CLIENT_ID, config.FENIX_REDIRECT_URI,
                                            config.FENIX_CLIENT_SECRET, config.FENIX_BASE_URL)
fenix_client = fenixedu.FenixEduClient(fen_config)

bot = commands.Bot(command_prefix=config.BOT_CMD_PREFIX)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


def get_auth_url(member):
    return fenix_client.get_authentication_url() + "state=" + member.id


def format_msg(msg, params):
    for tag, val in params:
        msg = msg.replace("{" + tag + "}", val)
    return msg


@bot.event
async def on_member_join(member):
    await member.create_dm()
    url = get_auth_url(member)
    await member.dm_channel.send(format_msg(config.MSG_JOIN, {'name': member.display_name, 'url': url}))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


async def auth_sucess(user):
    duser = bot.get_user(user.user_id)
    if duser is None:
        raise Exception()

    curriculum = fenix_client.get_person_curriculum(user)
    cadeiras = fenix_client.get_person_courses(user)
    person = fenix_client.get_person(user)

    guild = bot.get_guild(config.BOT_GUILD)
    roles = guild.roles



bot.run(config.BOT_TOKEN)
