from flask_mail import Message
import time
from .extensions import mail

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

from .views import connect, User
from .hash import hash_pw

mailer = Blueprint('mailer', __name__)

s = Serializer('secret key')


def change_pw(new_pw, email):
    local_session = connect()
    usr = local_session.query(User).filter_by(email=email).first()
    usr.pw = hash_pw(new_pw)
    local_session.commit()
    return



@ mailer.route('/send_confirm_email', methods=['GET', 'POST'])
def send_confirm_email():
    email = session["email"]
    token = s.dumps(email, salt='confirm_email')
    session.pop('email', None)
    msg = Message(sender='syuhas22@gmail.com', recipients=[email])
    msg.subject = 'Confirmation Email'
    link = url_for('mailer.confirm_email', token=token, _external=True)
    msg.html = render_template('confirm_email.html', link=link)
    mail.send(msg)
    return redirect(url_for('views.login'))
    

@ mailer.route('confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    try:
        email = s.loads(token, salt='confirm_email', max_age=1800)
    except SignatureExpired:
        flash('Expired link. Please try again.')
        return redirect(url_for('views.signup'))
    except BadSignature:
        flash('Invalid link. Please try again.')
        return redirect(url_for('views.signup'))
    
    local_session = connect()
    usr = local_session.query(User).filter_by(email=email).first()
    print(usr.confirmed)
    usr.confirmed = True
    local_session.commit()
    flash('Email confirmed. Please login.')
    return redirect(url_for('views.login'))
    







@ mailer.route('/forgotpw', methods=['GET', 'POST'])
def forgotpw():
    if request.method == 'POST':
        em = request.form['em']
        local_session = connect()
        usr = local_session.query(User).filter_by(email=em).first()
        if usr is not None:
            token = s.dumps(em, salt='reset_pw')
            msg = Message(sender='syuhas22@gmail.com', recipients=[em])
            msg.subject = 'Password Reset'
            link = url_for('mailer.resetpw', token=token, _external=True)
            msg.html = render_template('forgot_pw.html', link=link)
            mail.send(msg)
            flash('Email sent. Please check your email and follow the link to reset your password.')
            return redirect(url_for('views.login'))
        else:
            flash('Email does not exist in system.')
            return redirect(url_for('mailer.forgotpw'))
    else:
        return render_template('forgot_pw_form.html')



@ mailer.route('/resetpw/<token>', methods=['GET', 'POST'])
def resetpw(token):
    try:
        email = s.loads(token, salt='reset_pw', max_age=1800)
    except SignatureExpired:
        flash('Expired link. Please request a new link.')
        return redirect(url_for('mailer.forgotpw'))
    except BadSignature:
        flash('Invalid link. Please request a new link.')
        return redirect(url_for('mailer.forgotpw'))

    if request.method == 'POST':
        new_pw = request.form['pw1']
        confirm_pw = request.form['pw2']
        if new_pw == confirm_pw:
            change_pw(new_pw, email)      
            flash('Password successfully changed.')
            return redirect(url_for('views.login'))
        elif new_pw == '' or confirm_pw == '':
            flash('Please enter both passwords.')
            return redirect(url_for('mailer.resetpw', token=token))
        else:
            flash('Passwords do not match.')
            return redirect(url_for('mailer.resetpw', token=token))
    else:
        return render_template('new_pw_form.html', email=email)
        
