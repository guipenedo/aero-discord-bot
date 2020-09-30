import asyncio
import time
from threading import Thread
from database import User
from database import session, Cadeira
from fenix import fenix_client
from .utils import not_aero, criar_cadeira
import config
import bot


class TaskNewUser(Thread):
    def __init__(self):
        super(TaskNewUser, self).__init__()
        self.run_thread = True

    def run(self):
        print("starting thread")
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._run())
        loop.close()

    async def _run(self):
        self.run_thread = True
        print("starting async task")
        while self.run_thread:
            print("running")
            users = session.query(User).filter(User.initialized==False).all()
            guild = bot.bot.get_guild(config.BOT_GUILD)
            for user in users:
                print(user.user_id)
                duser = guild.get_member(user.user_id)
                if duser is None:
                    print("is none")
                    session.delete(user)
                    continue

                person = fenix_client.get_person(user)
                if not_aero(person):
                    print("not aero")
                    await duser.send("Neste momento, os registos estão limitados aos estudantes de aeroespacial. Sorry ;(")
                    session.delete(user)
                    continue
                print("aero")
                # curriculum = fenix_client.get_person_curriculum(user)
                cadeiras = fenix_client.get_person_courses(user)

                new_roles = []
                for cadeira in cadeiras["enrolments"]:
                    cadeira_id = int(cadeira["id"])
                    db_cadeira = session.query(Cadeira).get(cadeira_id)
                    if db_cadeira is None:
                        print("criando cadeira")
                        db_cadeira = criar_cadeira(cadeira_id)
                    new_roles.append(guild.get_role(db_cadeira.role_id))
                if new_roles:
                    await duser.add_roles(new_roles)

                user.initialized = True
                session.commit()

                await duser.send("Auth concluída!")
            if len(users):
                session.commit()
            time.sleep(10)

    def stop(self):
        self.run_thread = False
