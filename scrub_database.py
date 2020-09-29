from database import Session, engine, Base, discordUser

Base.metadata.create_all(engine)
session = Session()


# session.query(discordUser).delete()
# session.commit()

users = session.query(discordUser).all()
for x in users:

    print (x.discordUsername)


    # if x.discordUsername[:-2] == 'Ð&#383;&#321;µþ1#2048':
    #     print('hey')
    #     session.delete(x)
    #     session.commit()
    





    # print(x.discordUsername)
    # print(x.access_token)
    # print(x.refresh_token)
    # print(x.token_expires)
