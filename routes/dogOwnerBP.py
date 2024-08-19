from flask import Blueprint
from controllers.dogOwnerControllers import login, save

dog_owner_blueprint = Blueprint('owner_bp', __name__)

dog_owner_blueprint.route('/login', methods=['POST'])(login)
dog_owner_blueprint.route('/', methods=['POST'])(save)