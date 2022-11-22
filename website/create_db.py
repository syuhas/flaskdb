from views import User, Base, engine

from views import connect


""" Base.metadata.create_all(engine) """


""" sesh = connect()

email = 'steve@gmail.com'

usrem = sesh.query(User).filter_by(email=email).first()

print(usrem.email)
print(usrem.pw)
print(usrem.id)
print(usrem.username)

for x in usrem:
    print(x) """

