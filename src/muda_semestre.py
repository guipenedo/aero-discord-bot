import discord
from discord.ext import commands

import config
from database import init_db, session_scope, User

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.BOT_CMD_PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    init_db()
    """
    cadeiras_cats = []
    for cat in guild.categories:
        if cat.name.lower() == config.COURSES_DISC_CATEGORY_NAME.lower():
            cadeiras_cats.append(cat)

    with session_scope() as session:
        cadeiras = session.query(Cadeira).all()
        print("Preparing to delete", len(cadeiras), "cadeiras.")
        for cadeira in cadeiras:
            channel = bot.get_channel(cadeira.channel_id)
            if channel:
                await channel.delete()
            for cat in cadeiras_cats:
                for dchannel in cat.channels:
                    if dchannel.name == cadeira.name.lower().replace(' ', '-'):
                        await dchannel.delete()
            role = guild.get_role(cadeira.role_id)
            if role:
                await role.delete()
            time.sleep(1)
        print("deleting all")
        return
        num_rows_deleted = session.query(Cadeira).delete()
        return
        print("Deleted", num_rows_deleted, "cadeiras.")"""
    with session_scope() as session:
        # mark all as not updated
        session.query(User).filter(User.initialized).update({User.new_semester: False})
        print("All users set to wait for new_semester update")
    await bot.logout()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(config.BOT_CMD_ERROR)


bot.run(config.BOT_TOKEN)
