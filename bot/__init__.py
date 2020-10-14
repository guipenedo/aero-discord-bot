from discord.ext import commands
import discord

import config
from fenix import fenix_client
from database import init_db
from .utils import format_msg

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.BOT_CMD_PREFIX, intents=intents)

cogs = ['bot.task_rss', 'bot.task_user_roles']

for extension in cogs:
    bot.load_extension(extension)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    #embed = discord.Embed(title="Bem-vindo 🥳",
    #                      description="Com o objetivo de centralizar todos os grupos e chats num único sítio, criou-se este servidor de Discord de MEAer 🚀.\n\nO único requisto é teres passado pelo curso de Aeroespacial algures na tua vida e o nosso bot tratará de te atribuir aos canais apropriados.\n\nPara além de teres acesso a vários canais referentes às cadeiras em que estás inscrito, poderás ainda comunicar com os melhores grupos do Técnico, os de Aeroespacial 💕: **AeroLiga** ⚽, **AeroTéc** 🛩️, **CPAero** 🐧, e **Delegados** 🦸.\n\nHaverá também canais para convívio 🤼, gaming 🕹️ e outras atividades 🤷.\n\nSe precisarem de ajuda, falem com um <@&764146251296931860>.", color=0xFF0022)
    # await bot.get_channel(764152890771898438).send(embed=embed)
    # embed=discord.Embed(title="Sobre o Bot :robot:", description="O <@601401283009577001> é um bot de discord criado por estudantes de aeroespacial. O bot, através da vossa conta do fénix <:ist:601199845801459742>, adiciona-vos ao channel de discussão do vosso ano e aos channels das cadeiras em que estão inscritos.\n\nCada cadeira tem dois channels:\n:arrow_forward: um de ***discussão*** :speech_left:, para discussão geral da cadeira\n:arrow_forward: um de ***anúncios*** :loudspeaker:, onde o bot publica em tempo real os anúncios do fénix <:ist:601199845801459742>\n\n:bangbang: Os vossos dados do fénix, para além das cadeiras e ano, não é gravada em nenhum local.\n\n[Todo o código do bot está disponível no GitHub, e aberto a contribuições.](https://github.com/guipenedo/aero-discord-bot)", color=0x9c3eff)
    # await bot.get_channel(764152890771898438).send(embed=embed)
    init_db()


def get_auth_url(member):
    return fenix_client.get_authentication_url(str(member.id))


@bot.event
async def on_member_join(member):
    url = get_auth_url(member)
    await member.send(format_msg(config.MSG_JOIN, {'name': member.display_name, 'url': url}))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(config.BOT_CMD_ERROR)

bot.run(config.BOT_TOKEN)
