from flask_bcrypt import Bcrypt
from flask import Blueprint, render_template

hash = Blueprint('hash', __name__)


bcrypt = Bcrypt()


def hash_pw(pw):
    return bcrypt.generate_password_hash(pw)

def check_pw(hash, pw):
    return bcrypt.check_password_hash(hash, pw)

""" user = 'steve'
passw = 'funstuff'
local_session = connect()                   ### how the dehashing works
                                                          

usr = local_session.query(User).filter_by(username=user).first()

print(check_pw(usr.pw, passw)) """