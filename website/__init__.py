
import os

from flask import Flask

from .extensions import mail


def create_application():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    with app.app_context():
        from .views import views        
        from .hash import hash        
        from .mailer import mailer
        from .auth import auth
        from .database import database
        from .profiles import profiles
        from .forms import forms

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(hash)
        app.register_blueprint(mailer, url_prefix='/')
        app.register_blueprint(auth)
        app.register_blueprint(database)
        app.register_blueprint(profiles)
        app.register_blueprint(forms)

    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'syuhas22@gmail.com'
    app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_PW')

    
    print(app.config['MAIL_PASSWORD'])


    mail.init_app(app)

    

    return app
