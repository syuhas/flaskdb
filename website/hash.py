from flask_bcrypt import Bcrypt

from flask import Blueprint, render_template

hash = Blueprint('hash', __name__)


bcrypt = Bcrypt()



def hash_pw(pw):
    return bcrypt.generate_password_hash(pw, rounds=12)

def check_pw(hash, pw):
    return bcrypt.check_password_hash(hash, pw)

