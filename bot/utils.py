import config
from bot import bot
from fenix import fenix_client
from database import session, Cadeira
import discord


async def criar_cadeira(cadeira_id):
    # Obter informação da cadeira
    cadeira = fenix_client.get_course(cadeira_id)
    if cadeira is None:
        raise Exception()

    name = cadeira["name"].lower().replace(' ', '-')   # TODO: is this necessary?
    guild = bot.get_guild(config.BOT_GUILD)

    # TODO: verificar se o role já existe
    # Criar role
    drole = await guild.create_role(name)

    # TODO: verificar se já há um channel com o mesmo nome
    # Criar channel
    # TODO: é preciso pôr todos os outros roles a False?
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        drole: discord.PermissionOverwrite(read_messages=True)
    }
    category = "temp"       # TODO: get year
    dchannel = await guild.create_text_channel(name, overwrites=overwrites, category=category)
    
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
