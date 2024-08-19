from flask import Blueprint
from controllers.profileControllers import save, find_all, update, delete, find_by_id

profile_blueprint = Blueprint('profile_bp', __name__)

profile_blueprint.route('/', methods=['POST'])(save)
profile_blueprint.route('/', methods=['GET'])(find_all)
profile_blueprint.route('/profiles/<int:profile_id>', methods=['GET'])(find_by_id)
profile_blueprint.route('/profiles/<int:profile_id>', methods=['PUT'])(update)
profile_blueprint.route('/profiles/<int:profile_id>', methods=['DELETE'])(delete)
