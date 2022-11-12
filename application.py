from datetime import datetime

import sqlalchemy as db
from flask import flash, redirect, render_template, request, session, url_for
from sqlalchemy import (VARCHAR, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, create_engine, text)
from sqlalchemy.orm import declarative_base, sessionmaker

from website import create_application

application = create_application()


DATABASE_URL = 'mysql+pymysql://syuhas:funstuff@mydb.cypnvtxsedui.us-east-1.rds.amazonaws.com:3306'

Base = declarative_base()

engine = create_engine(DATABASE_URL, echo=True)




class User(Base):
    __tablename__ = 'users'
    # 'nullable=false': this means that the column cannot be null or empty
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    email = Column(String(120), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"User username={self.user} email={self.email}"


def connect():
    Session = sessionmaker()
    local_session = Session(bind=engine)
    with engine.connect() as connection:
        connection.execute(f"CREATE DATABASE IF NOT EXISTS {User.__tablename__}")
        connection.execute(f"USE {User.__tablename__}")
    return local_session



def create_user(nm, em):
    local_session = connect()
    new_user = User(username=nm, email=em)
    local_session.add(new_user)
    local_session.commit()
    return




















""" Base.metadata.create_all(engine) """

""" @ application.route('/') #home template
def home():
    return render_template('home.html')


@ application.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["username"] = request.form["nm"]
        session["useremail"] = request.form["em"]
        return redirect(url_for('user'))
    else:
        return render_template('login.html') """


""" @ application.route('/user') #user management
def user():
    if "username" in session and "useremail" in session:
        user = session["username"]
        em = session["useremail"]
        
        usrs = local_session.query(User).all()
        for usr in usrs:
            if user == usr.username or em == usr.email:
                session.pop('username', None)
                session.pop('useremail', None)
                flash("User Already Exists")
                return redirect(url_for('login'))

        create_user(user, em)
        flash("Welcome " + user)
        return render_template('login.html', name = user, email = em) """


@application.route('/') # lists users route
def listusers():
    local_session = connect()
    usrs = local_session.query(User).all()
    return render_template('listusers.html', usrs = usrs)


""" @ application.route('/logout') #logout route
def logout():
    if "username" in session and "useremail" in session:
        flash("Logged out successfully", "messages")
    session.pop('username', None)
    session.pop('useremail', None)
    return redirect(url_for('login')) """


if __name__ == "__main__":
    application.run(debug = True)
