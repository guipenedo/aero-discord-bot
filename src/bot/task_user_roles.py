from discord import Forbidden
from discord.ext import tasks, commands

import config
from database import session_scope, Cadeira, User
from fenix import fenix_client
from .utils import not_aero, get_first_enrollment, get_or_create_year_role, format_msg, \
    get_or_create_role, process_enrollments


class TaskNewUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.newusers.start()

    def cog_unload(self):
        self.newusers.cancel()

    async def update_users(self):
        with session_scope() as session:
            users = session.query(User).filter(User.initialized == False).all()
            guild = self.bot.get_guild(config.BOT_GUILD)

            all_cadeiras_roles = []
            # if we are updating existing users, remove all cadeiras first
            if users:
                all_cadeiras_roles = [guild.get_role(x.role_id) for x in session.query(Cadeira).all()]

            # Loop through users
            for user in users:
                try:
                    # Delete user from db if not in the guild
                    duser = guild.get_member(user.user_id)
                    if duser is None:
                        session.delete(user)
                        continue
                    person = fenix_client.get_person(user)
                    if "error" in person and "accessTokenInvalid" in person["error"]:
                        session.delete(user)
                        continue
                    if not_aero(person):
                        await duser.send(config.MSG_AERO_ONLY)
                        session.delete(user)
                        continue

                    cadeiras = fenix_client.get_person_courses(user)
                    user_roles = duser.roles
                    # look for roles from old cadeiras
                    remove_roles = []
                    for role in user_roles:
                        # check if this is a course role and not some random role
                        if role in all_cadeiras_roles:
                            remove_roles.append(role)
                    # remove them
                    if remove_roles:
                        await duser.remove_roles(*remove_roles)

                    # first timer. add to the correct year discussion channel
                    first_enroll = get_first_enrollment(person)
                    if first_enroll:
                        year_role = await get_or_create_year_role(first_enroll, self.bot)
                        await duser.add_roles(year_role)
                        await duser.send(format_msg(config.MSG_ADDED_CHANNEL_YEAR, {'first_enroll': first_enroll}))

                    print("Welcoming " + person["name"])
                    names = person["name"].split(" ")
                    await duser.edit(nick=names[0] + " " + names[-1])

                    # Loop through courses
                    await process_enrollments(cadeiras, duser, self.bot)

                    user.initialized = True
                    auth_role = await get_or_create_role(guild, config.ROLE_AUTH_NAME)
                    await duser.add_roles(auth_role)
                    await duser.send(config.BOT_AUTH_SUCCESS)
                except Forbidden:
                    pass

    # this task adds new users
    @tasks.loop(seconds=config.NEW_USER_INTERVAL)
    async def newusers(self):
        await self.update_users()

    @newusers.before_loop
    async def before_newusers(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(TaskNewUser(bot))
