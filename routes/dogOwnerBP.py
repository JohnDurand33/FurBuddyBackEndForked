from flask import Blueprint
from controllers.dogOwnerControllers import login, save, update_owner, delete_owner

dog_owner_blueprint = Blueprint('owner_bp', __name__)

dog_owner_blueprint.route('/login', methods=['POST'])(login)
dog_owner_blueprint.route('/', methods=['POST'])(save)
dog_owner_blueprint.route('/owners/<int:id>', methods=['PUT'])(update_owner)
dog_owner_blueprint.route('/owners/<int:id>', methods=['DELETE'])(delete_owner)
