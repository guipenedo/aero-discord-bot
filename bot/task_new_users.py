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
        self.run_thread = True
        while self.run_thread:
            users = session.query(User).filter(User.initialized is False).all()
            guild = bot.bot.get_guild(config.BOT_GUILD)
            for user in users:
                duser = guild.get_member(user.user_id)
                if duser is None:
                    session.delete(user)
                    continue

                person = fenix_client.get_person(user)
                if not_aero(person):
                    duser.send("Neste momento, os registos estão limitados aos estudantes de aeroespacial. Sorry ;(")
                    session.delete(user)
                    continue

                # curriculum = fenix_client.get_person_curriculum(user)
                cadeiras = fenix_client.get_person_courses(user)

                new_roles = []
                for cadeira in cadeiras["enrolments"]:
                    cadeira_id = int(cadeira["id"])
                    db_cadeira = session.query(Cadeira).get(cadeira_id)
                    if db_cadeira is None:
                        db_cadeira = criar_cadeira(cadeira_id)
                    new_roles.append(guild.get_role(db_cadeira.role_id))
                duser.add_roles(new_roles)

                user.initialized = True
                session.commit()

                duser.send("Auth concluída!")
            if len(users):
                session.commit()
            time.sleep(10)

    def stop(self):
        self.run_thread = False
