from flask import render_template
from views import *
def index():
    return render_template('index.html')