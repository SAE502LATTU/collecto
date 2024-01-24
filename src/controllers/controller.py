from flask import render_template
from views import *
def index():
    return render_template('index.html')

def audit():
    return render_template('audit.html')