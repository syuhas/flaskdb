from datetime import datetime


from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import (VARCHAR, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, create_engine, text)
from sqlalchemy import delete
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
    confirmed = Column(Boolean, default=False)
    date_created = Column(DateTime, default=datetime.utcnow, nullable=False)


with engine.connect() as connection:                                   # initial connection to the databse using the table
    connection.execute(text(f'CREATE DATABASE IF NOT EXISTS {User.__tablename__}'))
    connection.execute(text(f'USE {User.__tablename__}'))




def connect():                                          # reconnects and loads fresh data from db, returns connection as local session
    Session = sessionmaker()                            # use to make sure no stale data
    local_session = Session(bind=engine)
    try:
        with engine.connect() as connection:
            connection.execute(f"USE {User.__tablename__}")
    except:
        flash('Database connection error, please try again later')
        return redirect(url_for('views.login'))
    return local_session



def create_user(nm, pw, email):                                # creates user; reconnects and adds user to the database
    local_session = connect()
    new_user = User(username=nm, pw=pw, email=email, confirmed=False)
    local_session.add(new_user)
    local_session.commit()
    return



@ views.route('/')                                      # home template
def home():
    
    return render_template('home.html')


@ views.route('/signup', methods=['GET', 'POST'])       # signup template
def signup():
    if request.method == 'POST':
        username = request.form.get('nm')
        pass1 = request.form['pw1']
        pass2 = request.form['pw2']
        email1 = request.form['em1']
        email2 = request.form['em2']
        if username == '' or pass1 == '' or pass2 == '' or email1 == '' or email2 == '':
            flash('All fields are required', category='error')
            return redirect(url_for('views.signup'))
        elif pass1 != pass2 and email1 == email2:
            flash("Passwords do not match.")
            return redirect(url_for('views.signup'))
        elif pass1 == pass2 and email1 != email2:
            flash("Emails do not match.")
            return redirect(url_for('views.signup'))
        elif pass1 != pass2 and email1 != email2:
            flash("Passwords and Emails do not match.")
            return redirect(url_for('views.signup'))
        elif pass1 == pass2 and email1 == email2:
            password = hash_pw(pass1)
            email = email1
            session["email"] = email
            local_session = connect()
            usrs = local_session.query(User).all()
            for usr in usrs:
                if username == usr.username:
                    flash("User Already Exists")
                    return redirect(url_for('views.signup'))
                elif username == usr.email:
                    flash("Email Already Exists")
                    return redirect(url_for('views.signup'))
            create_user(username, password, email)
            return redirect(url_for('mailer.send_confirm_email'))
    else:
        return render_template('signup.html')

@ views.route('/newuser')                              # handler for new user signup
def newuser(username, email, pw):
    create_user(username, pw, email)
    flash("Welcome " + user + ". Please Sign In.")
    session.pop('username', None)
    session.pop('password', None)
    session.pop('email', None)
    return redirect(url_for('views.login'))
    


@ views.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["username"] = request.form["nm"]
        session["password"] = request.form["pw"]
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
        usrem = local_session.query(User).filter_by(email=user).first()
        if usr is None and usrem is None:
            flash("User not found")
            session.pop('username', None)
            session.pop('password', None)
            return redirect(url_for('views.login'))
        elif usr is None and usrem is not None:
            user = usrem.username
            hashed_check = check_pw(usrem.pw, password)
        elif usr is not None and usrem is None:
            user = usr.username
            hashed_check = check_pw(usr.pw, password)
            
        if not hashed_check:
            flash("Password is incorrect")
            session.pop('username', None)
            session.pop('password', None)
            return redirect(url_for('views.login'))
        else:
            if usr.confirmed:
                flash("Welcome Back, " + user)
                session.pop('password', None)
                return redirect(url_for('views.login'))
            elif not usr.confirmed:
                session.pop('username', None)
                session.pop('password', None)
                return redirect(url_for('views.unconfirmed'))
    else:
        return redirect(url_for('views.login'))


@ views.route('/userprofile', methods=["POST", "GET"])
def userprofile():
    if request.method == "POST":
        local_session = connect()
        usr = local_session.query(User).filter_by(username=session['username']).first()

        if request.form['em'] != '':
            usr.email = request.form['em']
            flash("Email Updated")
            
        if request.form['fn'] != '':
            usr.firstname = request.form['fn']
            flash("First Name Updated")
            
        if request.form['ln'] != '':
            usr.lastname = request.form['ln']
            print(usr.lastname)
            flash("Last Name Updated")

        if request.form["old-pw"] != '' or request.form["new-pw1"] != '' or request.form["new-pw2"] != '':
            if request.form["old-pw"] == '':
                flash("Please enter your current password.")
                return redirect(url_for('views.userprofile'))
            if request.form["new-pw1"] == '' or request.form["new-pw1"] == '':
                flash("Please enter and confirm new password.")
                return redirect(url_for('views.userprofile'))
            else:
                old_pw = request.form["old-pw"]
                if request.form["new-pw1"] == request.form["new-pw2"] and check_pw(usr.pw, old_pw):
                    print(check_pw(usr.pw, old_pw))
                    new_pw = request.form['new-pw1']
                    usr.pw = hash_pw(new_pw)
                    flash("Password Successfully Changed.")
                elif not check_pw(usr.pw, old_pw):
                    flash("Incorrect Password")
                    return redirect(url_for('views.userprofile'))
                else:
                    flash("Passwords do not match. Please try again.")
                    return redirect(url_for('views.userprofile'))
        
        
        local_session.commit()
        return redirect(url_for('views.userprofile'))
    else:
        local_session = connect()
        usr = local_session.query(User).filter_by(username=session['username']).first()
        return render_template('userprofile.html', username=usr.username,  email=usr.email, firstname=usr.firstname, lastname=usr.lastname)



@ views.route('/unconfirmed')
def unconfirmed():
    return render_template('unconfirmed.html')










@ views.route('/listusers')                              # list users template
def listusers():
    local_session = connect()
    usrs = local_session.query(User).all()
    return render_template('listusers.html', usrs = usrs)


@ views.route('/logout')                                # handler for logout
def logout():
    flash("Logged out successfully", "messages")
    session.pop('username', None)
    return redirect(url_for('views.login'))