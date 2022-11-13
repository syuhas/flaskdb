from flask import Flask



def create_application():
    app = Flask(__name__)
    app.config['SECRET KEY'] = 'asdasdasd'
    app.secret_key = '04241985'

    from .views import views
    
    app.register_blueprint(views, url_prefix='/')
    


    return app
