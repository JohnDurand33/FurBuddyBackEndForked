from flask import Blueprint
from controllers.profileControllers import save, find_all, update_profile, delete_profile, find_by_id, get_profile_with_owner

profile_blueprint = Blueprint('profile_bp', __name__)

profile_blueprint.route('/owner/<int:owner_id>/profiles', methods=['POST'])(save)
profile_blueprint.route('/owner/<int:owner_id>/profiles', methods=['GET'])(find_all)
profile_blueprint.route('/owner/<int:owner_id>/profiles/<int:profile_id>', methods=['GET'])(find_by_id)
profile_blueprint.route('/owner/<int:owner_id>/profiles/<int:profile_id>', methods=['PUT'])(update_profile)
profile_blueprint.route('/owner/<int:owner_id>/profiles/<int:profile_id>', methods=['DELETE'])(delete_profile)
profile_blueprint.route('/owner/<int:owner_id>/profiles/<int:profile_id>/details', methods=['GET'])(get_profile_with_owner)


