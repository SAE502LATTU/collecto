from flask import Blueprint
from controllers.controller import index

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(index)