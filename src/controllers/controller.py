from flask import render_template
from .server_stats import get_server_stats

def index():
    server_stats = get_server_stats()
    return render_template('index.html', server_stats=server_stats)
