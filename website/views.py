from datetime import datetime


from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import (VARCHAR, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, create_engine, text)
from sqlalchemy.orm import declarative_base, sessionmaker
from .hash import hash_pw, check_pw

views = Blueprint('views', __name__)

DATABASE_URL = 'mysql+pymysql://syuhas:funstuff@mydb.cypnvtxsedui.us-east-1.rds.amazonaws.com:3306'

Base = declarative_base()

engine = create_engine(DATABASE_URL, echo=True)




class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False, unique=True)      # 'nullable=false': this means that the column cannot be null or empty
    pw = Column(String(80), nullable=False)
    email = Column(String(120))
    firstname = Column(String(80))
    lastname = Column(String(80))
    date_created = Column(DateTime, default=datetime.utcnow, nullable=False)


with engine.connect() as connection:                                   # initial connection to the databse using the table
    connection.execute(text(f'CREATE DATABASE IF NOT EXISTS {User.__tablename__}'))
    connection.execute(text(f'USE {User.__tablename__}'))




def connect():                                          # reconnects and loads fresh data from db, returns connection as local session
    Session = sessionmaker()                            # use to make sure no stale data
    local_session = Session(bind=engine)
    with engine.connect() as connection:
        connection.execute(f"USE {User.__tablename__}")
    return local_session



def create_user(nm, pw):                                # creates user; reconnects and adds user to the database
    local_session = connect()
    new_user = User(username=nm, pw=pw)
    local_session.add(new_user)
    local_session.commit()
    return





@ views.route('/')                                      # home template
def home():
    return render_template('home.html')


@ views.route('/signup', methods=['GET', 'POST'])       # signup template
def signup():
    if request.method == 'POST':
        pass1 = request.form['pw1']
        pass2 = request.form['pw2']
        if pass1 == pass2:
            session["username"] = request.form['nm']
            session["password"] = hash_pw(pass1)
            return redirect(url_for('views.newuser'))
        else:
            flash("Passwords do not match")
            return redirect(url_for('views.signup'))
    else:
        return render_template('signup.html')

@ views.route('/newuser')                              # handler for new user signup
def newuser():
    if "username" in session:
        user = session["username"]
        pw = session["password"]
        local_session = connect()
        usrs = local_session.query(User).all()
        for usr in usrs:
            if user == usr.username:
                session.pop('username', None)
                session.pop('password', None)
                flash("User Already Exists")
                return redirect(url_for('views.signup'))
        create_user(user, pw)
        flash("Welcome " + user)
        return render_template('login.html', name = user)
    else:
        redirect(url_for('views.signup'))


@ views.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["username"] = request.form["nm"]
        session["password"] = request.form["pw"]
        print(session["password"])
        return redirect(url_for('views.user'))
    else:
        return render_template('login.html')


@ views.route('/user')                              # handler for existing user
def user():
    if "username" in session:
        user = session["username"]
        password = session["password"]
        local_session = connect()
        usr = local_session.query(User).filter_by(username=user).first()
        if usr is None:
            flash("Username not found")
            session.pop('username', None)
            session.pop('password', None)
            return redirect(url_for('views.login'))
        hashed_check = check_pw(usr.pw, password)
        if not hashed_check:
            flash("Password is incorrect")
            session.pop('username', None)
            session.pop('password', None)
            return redirect(url_for('views.login'))
        else:
            flash("Welcome Back, " + user)
            return redirect(url_for('views.login'))
    else:
        return redirect(url_for('views.login'))

@views.route('userprofile')
def userprofile():
    return render_template('userprofile.html')


@views.route('/listusers')                              # list users template
def listusers():
    local_session = connect()
    usrs = local_session.query(User).all()
    return render_template('listusers.html', usrs = usrs)


@ views.route('/logout')                                # handler for logout
def logout():
    flash("Logged out successfully", "messages")
    session.pop('username', None)
    return redirect(url_for('views.login'))