from flask import Blueprint
from controllers.profileControllers import save_profile, find_by_id, update_profile_info, delete_profile_info

profile_blueprint = Blueprint('profile_bp', __name__)

profile_blueprint.route('/owner/<int:owner_id>/profiles', methods=['POST'])(save_profile)
profile_blueprint.route('/owner/<int:owner_id>/profiles/<int:profile_id>', methods=['GET'])(find_by_id)
profile_blueprint.route('/owner/<int:owner_id>/profiles/<int:profile_id>', methods=['PUT'])(update_profile_info)
profile_blueprint.route('/owner/<int:owner_id>/profiles/<int:profile_id>', methods=['DELETE'])(delete_profile_info)

# profile_blueprint.route('/owner/<int:owner_id>/profiles', methods=['GET'])(get_all_profiles)
# profile_blueprint.route('/owner/<int:owner_id>/profiles/<int:profile_id>/details', methods=['GET'])(get_profile_with_owner)


