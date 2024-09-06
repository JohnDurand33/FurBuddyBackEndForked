from flask import Blueprint
from controllers.dogOwnerControllers import save, login, show_owner_info, update_owner, delete_owner

dog_owner_blueprint = Blueprint('owner_bp', __name__)


dog_owner_blueprint.route('/', methods=['POST', 'OPTIONS'])(save)
dog_owner_blueprint.route('/login', methods=['POST', 'OPTIONS'])(login)
dog_owner_blueprint.route('/owners/current', methods=['GET', 'OPTIONS'])(show_owner_info)
dog_owner_blueprint.route('/owners/current', methods=['PUT', 'OPTIONS'])(update_owner)
dog_owner_blueprint.route('/owners/current', methods=['DELETE', 'OPTIONS'])(delete_owner)