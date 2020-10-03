import config
from fenix import fenix_client
from database import session, Cadeira
import discord


async def get_or_create_category(guild, name, perms):
    for cat in guild.categories:
        if cat.name.lower() == name.lower():
            return cat
    overwrites = {
        guild.default_role: perms
    }
    return await guild.create_category(name, overwrites=overwrites)


async def get_or_create_role(guild, name):
    for drole in guild.roles:
        if drole.name == name:
            return drole
    return await guild.create_role(name=name)


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
    drole = await get_or_create_role(guild, name)

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


def not_aero(person):
    for role in person["roles"]:
        if role["type"] == "STUDENT":
            for reg in role["registrations"]:
                if int(reg["id"]) == int(config.FENIX_DEGREE):
                    return False
        elif role["type"] == "ALUMNI":
            for reg in role["concludedRegistrations"]:
                if int(reg["id"]) == int(config.FENIX_DEGREE):
                    return False
    return True


def format_msg(msg, params):
    for tag, val in params.items():
        msg = msg.replace("{" + tag + "}", val)
    return msg
