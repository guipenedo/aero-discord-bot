import config
from fenix import fenix_client
from database import session, Cadeira
import discord
import pytz
import time
import datetime


async def get_or_create_category(guild, name, perms):
    for cat in guild.categories:
        if cat.name.lower() == name.lower():
            return cat
    overwrites = {
        guild.default_role: perms
    }
    return await guild.create_category(name, overwrites=overwrites)


async def get_or_create_role(guild, name, **fields):
    for drole in guild.roles:
        if drole.name == name:
            return drole
    return await guild.create_role(name=name, **fields)


async def get_or_create_channel(guild, cat, name, overwrites):
    for dchannel in (guild.channels if cat is None else cat.channels):
        if dchannel.name == name:
            return dchannel
    overwrites[guild.default_role] = discord.PermissionOverwrite(read_messages=False, send_messages=False)
    return await guild.create_text_channel(name, overwrites=overwrites, category=cat)


async def criar_cadeira(cadeira_id, bot):
    # Obter informação da cadeira
    cadeira = fenix_client.get_course(cadeira_id)
    if cadeira is None:
        raise Exception()
    # Get name
    name = cadeira["name"].lower().replace(' ', '-')
    print("Creating cadeira " + name)

    # Get guild
    guild = bot.get_guild(config.BOT_GUILD)

    # Get feeds category
    feeds_cat = await get_or_create_category(guild, config.FEEDS_CATEGORY_NAME,
                                             discord.PermissionOverwrite(read_messages=False, send_messages=False))

    # Get courses discurssion category
    cadeiras_cat = await get_or_create_category(guild, config.COURSES_DISC_CATEGORY_NAME,
                                                discord.PermissionOverwrite(read_messages=False))

    # Criar role
    drole = await get_or_create_role(guild, name, colour=discord.Colour.dark_gold(), mentionable=True)

    # Criar channels
    await get_or_create_channel(guild, cadeiras_cat, name,
                                {drole: discord.PermissionOverwrite(read_messages=True, send_messages=True)})
    dchannel = await get_or_create_channel(guild, feeds_cat, name,
                                           {drole: discord.PermissionOverwrite(read_messages=True)})

    # Adicionar cadeira à base de dados
    db_cadeira = Cadeira(cadeira_id, cadeira["acronym"], cadeira["name"], cadeira["academicTerm"],
                         cadeira["announcementLink"], dchannel.id, drole.id)
    session.add(db_cadeira)
    session.commit()

    return db_cadeira


async def get_or_create_year_role(year, bot):
    # Get guild
    guild = bot.get_guild(config.BOT_GUILD)

    # Get years discussion category
    years_cat = await get_or_create_category(guild, config.YEARS_DISC_CATEGORY_NAME,
                                             discord.PermissionOverwrite(read_messages=False))

    # Get the role to see this year's channel
    drole = await get_or_create_role(guild, year, colour=discord.Colour.blue(), hoist=True, mentionable=True)

    # Make sure the channel exists
    await get_or_create_channel(guild, years_cat, year,
                                {drole: discord.PermissionOverwrite(read_messages=True, send_messages=True)})
    # Return the role
    return drole


# returns registrations (Student or alumni) for our FENIX_DEGREE
def get_registration(person):
    for role in person["roles"]:
        if role["type"] == "STUDENT":
            for reg in role["registrations"]:
                if int(reg["id"]) == int(config.FENIX_DEGREE):
                    return reg
        elif role["type"] == "ALUMNI":
            for reg in role["concludedRegistrations"]:
                if int(reg["id"]) == int(config.FENIX_DEGREE):
                    return reg
    return None


def not_aero(person):
    return get_registration(person) is None


def format_msg(msg, params):
    for tag, val in params.items():
        msg = msg.replace("{" + tag + "}", val)
    return msg


def get_first_enrollment(person):
    registration = get_registration(person)
    if registration is None:
        return None
    return min([x[-9:] for x in registration["academicTerms"]]).replace("/", "-")


def timezone(before):
    tz = pytz.timezone(config.TIMEZONE)
    date = time.mktime(before)  
    # naive datetimes are not associated to a timezone
    naive_date = datetime.datetime.fromtimestamp(date)
    # use tz.localize to make naive datetimes "timezone aware"
    after = tz.localize(naive_date, is_dst=None)
    return after.timetuple()


def get_auth_url(member):
    return fenix_client.get_authentication_url(str(member.id))
