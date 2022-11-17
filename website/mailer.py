from flask_mail import Message

from .extensions import mail

from flask import Blueprint, flash, redirect, render_template, request, session, url_for


mailer = Blueprint('mailer', __name__)



@mailer.route('/email', methods=['GET', 'POST'])
def email():
    if request.method == 'POST':
        em = request.form['em']
        msg = Message('Hello', sender='steve@digitalsteve.net', recipients=[em])
        msg.body = "This is a test email"
        mail.send(msg)
        flash('Email sent')
        return render_template('emailform.html')
    else:
        return render_template('emailform.html')