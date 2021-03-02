from discord.ext import commands
import discord

import config
from database import init_db, session_scope, User
from bot.utils import format_msg, get_auth_url

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.BOT_CMD_PREFIX, intents=intents)

cogs = ['bot.task_rss', 'bot.task_user_roles', 'bot.task_user_new_semester', 'bot.task_auth_link']

for extension in cogs:
    bot.load_extension(extension)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    init_db()


@bot.event
async def on_member_join(member):
    url = get_auth_url(member)
    await member.send(format_msg(config.MSG_JOIN, {'name': member.display_name, 'url': url}))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(config.BOT_CMD_ERROR)


@bot.command()
async def update(ctx):
    with session_scope() as session:
        user = session.query(User).filter(User.user_id == ctx.author.id).first()
        if user:
            user.new_semester = False
            await ctx.author.send("A tua lista de cadeiras será atualizada dentro de momentos.")
        else:
            await ctx.author.send(
                "Não foi possível encontrar o teu utilizador, mas podes voltar a fazer a autenticação aqui:\n"
                + get_auth_url(ctx.author))


bot.run(config.BOT_TOKEN)
