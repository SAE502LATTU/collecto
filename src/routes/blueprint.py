from flask import Blueprint
from controllers.controller import index, audit

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(index)

blueprint.route('/audit', methods=['GET'])(audit)
