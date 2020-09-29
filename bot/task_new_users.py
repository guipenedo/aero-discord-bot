import time
from threading import Thread
from database import User
from bot import bot
from database import session, Cadeira
from fenix import fenix_client
from .utils import not_aero, criar_cadeira
import config


class TaskNewUser(Thread):
    async def run(self):
        while True:
            users = session.query(User).filter(User.initialized is False).all()
            for user in users:
                duser = bot.get_user(user.user_id)
                if duser is None:
                    session.delete(user)
                    continue

                person = fenix_client.get_person(user)
                if not_aero(person):
                    await duser.create_dm()
                    await duser.dm_channel.send("Neste momento, os registos estão limitados aos estudantes de aeroespacial. Sorry ;(")
                    session.delete(user)
                    continue

                # curriculum = fenix_client.get_person_curriculum(user)
                cadeiras = fenix_client.get_person_courses(user)

                guild = bot.get_guild(config.BOT_GUILD)

                new_roles = []
                for cadeira in cadeiras["enrolments"]:
                    cadeira_id = int(cadeira["id"])
                    db_cadeira = session.query(Cadeira).get(cadeira_id)
                    if db_cadeira is None:
                        db_cadeira = await criar_cadeira(cadeira_id)
                    new_roles.append(guild.get_role(db_cadeira.role_id))
                duser.add_roles(new_roles)

                user.initialized = True
                session.commit()

                await duser.create_dm()
                await duser.dm_channel.send("Auth concluída!")
            if len(users):
                session.commit()
            time.sleep(10)
