
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from .hash import check_pw
from .database import connect, User
from .forms import Login






auth = Blueprint('auth', __name__)

def make_permanent():
    session.permanent = True
    session.modified = True



@ auth.route('/login', methods=["POST", "GET"])
def login():
    """ if request.method == "POST":
        session["username"] = request.form["nm"]
        session["password"] = request.form["pw"]
        return redirect(url_for('auth.user'))
    else: """
    username = None
    password = None
    form = Login()
    if form.validate_on_submit():
        username = form.username.data
        session["username"] = username
        form.username.data = ''
        password = form.password.data
        session["password"] = password
        form.password.data = ''
        return redirect(url_for('auth.user'))
    return render_template('login.html', username=username, password=password, form=form)


@ auth.route('/user')                              # handler for existing user
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
            return redirect(url_for('auth.login'))
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
            return redirect(url_for('auth.login'))
        else:
            if usr.confirmed:
                flash("Welcome Back, " + user)
                session.pop('password', None)
                return redirect(url_for('auth.login'))
            elif not usr.confirmed:
                session.pop('username', None)
                session.pop('password', None)
                return redirect(url_for('auth.unconfirmed'))
    else:
        return redirect(url_for('auth.login'))





@ auth.route('/logout')                                # handler for logout
def logout():
    flash("Logged out successfully", "messages")
    session.pop('username', None)
    return redirect(url_for('auth.login'))

@ auth.route('/unconfirmed')
def unconfirmed():
    return render_template('unconfirmed.html')

