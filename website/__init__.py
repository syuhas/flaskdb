from flask import Flask



def create_application():
    app = Flask(__name__)
    app.config['SECRET KEY'] = 'asdasdasd'
    app.secret_key = '04241985'

    


    return app
