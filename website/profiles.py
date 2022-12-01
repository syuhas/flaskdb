


from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from .hash import hash_pw, check_pw
from .database import connect, User

import boto3, botocore

from flask import current_app as app

from werkzeug.utils import secure_filename

import base64








profiles = Blueprint('profiles', __name__)

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config['S3_KEY'],
    aws_secret_access_key=app.config['S3_SECRET']
    )

def create_user(nm, pw, email):                                # creates user; reconnects and adds user to the database
    local_session = connect()
    new_user = User(username=nm, pw=pw, email=email, confirmed=False, profile_link='null')
    local_session.add(new_user)
    local_session.commit()
    return



@ profiles.route('/signup', methods=['GET', 'POST'])       # signup template
def signup():
    if request.method == 'POST':
        username = request.form.get('nm')
        pass1 = request.form['pw1']
        pass2 = request.form['pw2']
        email1 = request.form['em1']
        email2 = request.form['em2']
        if username == '' or pass1 == '' or pass2 == '' or email1 == '' or email2 == '':
            flash('All fields are required', category='error')
            return redirect(url_for('profiles.signup'))
        elif pass1 != pass2 and email1 == email2:
            flash("Passwords do not match.")
            return redirect(url_for('profiles.signup'))
        elif pass1 == pass2 and email1 != email2:
            flash("Emails do not match.")
            return redirect(url_for('profiles.signup'))
        elif pass1 != pass2 and email1 != email2:
            flash("Passwords and Emails do not match.")
            return redirect(url_for('profiles.signup'))
        elif pass1 == pass2 and email1 == email2:
            password = hash_pw(pass1)
            email = email1
            session["email"] = email
            local_session = connect()
            try:
                usrs = local_session.query(User).all()
                for usr in usrs:
                    if username == usr.username:
                        flash("User Already Exists")
                        return redirect(url_for('profiles.signup'))
                    elif username == usr.email:
                        flash("Email Already Exists")
                        return redirect(url_for('profiles.signup'))    
            except:
                pass
            create_user(username, password, email)
            flash("Thank you for creating your account. A confirmation link has been sent to your email address. Follow the link to confirm your account and log in.")
            return redirect(url_for('mailer.send_confirm_email'))
    else:
        return render_template('signup.html')

@ profiles.route('/newuser')                              # handler for new user signup
def newuser(username, email, pw):
    create_user(username, pw, email)
    flash("Welcome " + username + ". Please Sign In.")
    session.pop('username', None)
    session.pop('password', None)
    session.pop('email', None)
    return redirect(url_for('auth.login'))





@ profiles.route('/userprofile', methods=["POST", "GET"])
def userprofile():
    if request.method == "POST":

        if request.form.get('update') =='update':        
            local_session = connect()
            usr = local_session.query(User).filter_by(username=session['username']).first()            
                
            if request.form['fn'] != '':
                usr.firstname = request.form['fn']
                flash("First Name Updated")
                
            if request.form['ln'] != '':
                usr.lastname = request.form['ln']
                flash("Last Name Updated")

            if request.form['ph'] != '':
                usr.phone = request.form['ph']
                flash("Phone Number Updated")

            if request.form['lk'] != '':
                usr.linkedin = request.form['lk']
                flash("LinkedIn Profile Updated")

            if request.form["old-pw"] != '' or request.form["new-pw1"] != '' or request.form["new-pw2"] != '':
                if request.form["old-pw"] == '':
                    flash("Please enter your current password.")
                    return redirect(url_for('profiles.userprofile'))
                if request.form["new-pw1"] == '' or request.form["new-pw1"] == '':
                    flash("Please enter and confirm new password.")
                    return redirect(url_for('profiles.userprofile'))
                else:
                    old_pw = request.form["old-pw"]
                    if request.form["new-pw1"] == request.form["new-pw2"] and check_pw(usr.pw, old_pw):
                        print(check_pw(usr.pw, old_pw))
                        new_pw = request.form['new-pw1']
                        usr.pw = hash_pw(new_pw)
                        flash("Password Successfully Changed.")
                    elif not check_pw(usr.pw, old_pw):
                        flash("Incorrect Password")
                        return redirect(url_for('profiles.userprofile'))
                    else:
                        flash("Passwords do not match. Please try again.")
                        return redirect(url_for('profiles.userprofile'))
            """ data = {}
            img_file = request.files['file']
            flash(img_file)
            with open(img_file , mode='rb') as file:
                image = file.read()
            flash(image) """
            img = request.files['file']
            """ if img:
                img = secure_filename(img.filename)
                print(img.content_type)
                flash(img.filename)
                flash(img.mimetype)
                print(img.stream)
                print(img) """
            if img:
                img.filename = secure_filename(img.filename)
                output = s3_upload(img, app.config['S3_BUCKET'])
                local_session = connect()
                local_session.query(User).filter_by(username=session['username']).update({"profile_link": str(output)})


            if request.form['em1'] != '' or request.form['em2'] != '':
                if request.form["em1"] == '':
                    flash("Please enter your new email.")
                    return redirect(url_for('profiles.userprofile'))
                if request.form["em2"] == '':
                    flash("Please confirm your new email.")
                    return redirect(url_for('profiles.userprofile'))
                else:
                    if request.form["em1"] == request.form["em2"]:
                        session['email'] = request.form['em1']
                        local_session = connect()
                        usrs = local_session.query(User).all()
                        for usr in usrs:
                            if session['email'] == usr.email:
                                flash("Email Already Exists")
                                session.pop('email', None)
                                return redirect(url_for('profiles.userprofile'))
                            else:
                                usr = local_session.query(User).filter_by(username=session['username']).first()
                                usr.email = session['email']
                                usr.confirmed = False
                                session.pop('username', None)
                                local_session.commit()
                                flash("Email Updated. A confirmation link has been sent to your email address. Follow the link to confirm your account and log back in.")
                                return redirect(url_for('mailer.send_confirm_email'))

                    else:
                        flash("Emails do not match. Please try again.")
                        return redirect(url_for('profiles.userprofile'))
            
            local_session.commit()
            return redirect(url_for('profiles.userprofile'))

        elif request.form.get('delete') =='delete':
            local_session = connect()
            usr = local_session.query(User).filter_by(username=session['username']).first()
            local_session.delete(usr)
            session.pop('username', None)
            local_session.commit()
            flash("Account Deleted. Sorry to see you go. Feel free to sign up again!")
            return redirect(url_for('views.home'))
        else:
            flash("There was an error. Please try again.")
            return redirect(url_for('profiles.userprofile'))
    else:
        if 'username' in session:
            local_session = connect()
            usr = local_session.query(User).filter_by(username=session['username']).first()
            context = {
                'username': usr.username,
                'email': usr.email,
                'firstname': usr.firstname,
                'lastname': usr.lastname,
                'phone': usr.phone,
                'linkedin': usr.linkedin,
                'pic': usr.profile_link
            }
            print(context)
            return render_template('userprofile.html', **context)
        else:
            return redirect(url_for('auth.login'))

@ profiles.route('/s3_upload')
def s3_upload(img, bucket_name):
    # Uploads image to S3
    local_session = connect()
    usr = local_session.query(User).filter_by(username=session['username']).first()
    filename = f'{usr.username}_profile_img_{img.filename}'
    s3 = boto3.client('s3')

    s3.put_object(
        Bucket=bucket_name,
        Body=img,
        Key=filename,
        ContentType=img.content_type,
    )
    return "{}{}".format(app.config['S3_LOCATION'], filename)


    """ try:
        s3.upload_file(img, bucket_name, img.filename)
        flash("Image Updated")
    except Exception as e:
        print(e)
        return e """
    




@ profiles.route('/listusers')                              # list users template
def listusers():
    local_session = connect()
    usrs = local_session.query(User).all()
    return render_template('listusers.html', usrs = usrs)