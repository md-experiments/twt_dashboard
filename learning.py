from flask import Blueprint

learning_blueprint = Blueprint('learning', __name__)

@learning_blueprint.route('/new')
def home():
    return "Hello world"