from discord.ext import commands

import config
from .task_rss import TaskRss
from .task_new_users import TaskNewUser
from fenix import fenix_client

bot = commands.Bot(command_prefix=config.BOT_CMD_PREFIX)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    TaskRss().start()
    TaskNewUser().start()


def get_auth_url(member):
    return fenix_client.get_authentication_url() + "state=" + member.id


def format_msg(msg, params):
    for tag, val in params:
        msg = msg.replace("{" + tag + "}", val)
    return msg


@bot.event
async def on_member_join(member):
    print("sad debug msg")
    await member.create_dm()
    url = get_auth_url(member)
    await member.dm_channel.send(format_msg(config.MSG_JOIN, {'name': member.display_name, 'url': url}))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


bot.run(config.BOT_TOKEN)
