from flask import Flask
from flask_mail import Mail
from .extensions import mail


def create_application():
    app = Flask(__name__)
    app.config['SECRET KEY'] = 'asdasdasd'
    app.secret_key = '04241985'

    from .views import views
    app.register_blueprint(views, url_prefix='/')
    from .hash import hash
    app.register_blueprint(hash)
    from .mailer import mailer
    app.register_blueprint(mailer, url_prefix='/')

    
    app.config['MAIL_SERVER'] = "smtp.gmail.com"
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = "syuhas22@gmail.com"
    app.config['MAIL_PASSWORD'] = "vwjnsnxqotqqiuss"
    mail.init_app(app)

    return app
