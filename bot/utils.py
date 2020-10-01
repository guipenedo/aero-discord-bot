import config
from fenix import fenix_client
from database import session, Cadeira
import discord


async def criar_cadeira(cadeira_id, bot):
    # Obter informação da cadeira
    cadeira = fenix_client.get_course(cadeira_id)
    if cadeira is None:
        raise Exception()

    # Get name
    name = cadeira["name"].lower().replace(' ', '-')   # TODO: is this necessary?

    # Get guild
    guild = bot.get_guild(config.BOT_GUILD)

    # Criar role
    for drole in guild.roles:
        if drole.name == name:
            break
    else:
        drole = await guild.create_role(name=name)

    # Criar channel
    for dchannel in guild.channels:
        if dchannel.name == name:
            break
    else:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            drole: discord.PermissionOverwrite(read_messages=True)
        }
        dchannel = await guild.create_text_channel(name, overwrites=overwrites, category=None)

    # Adicionar cadeira à base de dados
    db_cadeira = Cadeira(cadeira_id, cadeira["acronym"], cadeira["name"], cadeira["academicTerm"], cadeira["announcementLink"], dchannel.id, drole.id)
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
