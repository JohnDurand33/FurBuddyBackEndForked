from flask import Blueprint
from controllers.profileControllers import save_profile, find_by_id, find_all, update_profile_info, delete_profile_info

profile_blueprint = Blueprint('profile_bp', __name__)

profile_blueprint.route('/owner/<int:owner_id>/profiles', methods=['POST', 'OPTIONS'])(save_profile)
profile_blueprint.route('/owner/<int:owner_id>/profiles/<int:profile_id>', methods=['GET', 'OPTIONS'])(find_by_id)
profile_blueprint.route('/owner/<int:owner_id>/profiles', methods=['GET', 'OPTIONS'])(find_all)
profile_blueprint.route('/owner/<int:owner_id>/profiles/<int:profile_id>', methods=['PUT', 'OPTIONS'])(update_profile_info)
profile_blueprint.route('/owner/<int:owner_id>/profiles/<int:profile_id>', methods=['DELETE', 'OPTIONS'])(delete_profile_info)




