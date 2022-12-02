
from flask import Blueprint, render_template

from .database import connect






views = Blueprint('views', __name__)





@ views.route('/')                                      # home template
def home():
    local_session = connect()
    return render_template('home.html')


