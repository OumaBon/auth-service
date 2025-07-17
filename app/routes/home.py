from flask import render_template
from . import api 




@api.route('/', methods=["GET"])
def get_home():
    return render_template('home.html')