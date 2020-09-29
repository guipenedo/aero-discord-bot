import config


def criar_cadeira(cadeira_id):
    # TODO: sacar info da cadeira do fenix, colocar na db, criar channel e role
    return


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
