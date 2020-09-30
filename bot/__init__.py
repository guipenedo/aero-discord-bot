from discord.ext import commands
import discord

import config
from fenix import fenix_client

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.BOT_CMD_PREFIX, intents=intents)

cogs = ['bot.task_rss', 'bot.task_new_users']

for extension in cogs:
    bot.load_extension(extension)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


def get_auth_url(member):
    return fenix_client.get_authentication_url() + "state=" + str(member.id)


def format_msg(msg, params):
    for tag, val in params.items():
        msg = msg.replace("{" + tag + "}", val)
    return msg


@bot.event
async def on_member_join(member):
    url = get_auth_url(member)
    await member.send(format_msg(config.MSG_JOIN, {'name': member.display_name, 'url': url}))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(config.BOT_TOKEN)
