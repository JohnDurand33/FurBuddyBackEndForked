from flask import Blueprint
from controllers.profileControllers import save_profile, find_by_id, find_all, update_profile_info, delete_profile_info

profile_blueprint = Blueprint('profile_bp', __name__)


profile_blueprint.route('/profiles', methods=['POST'])(save_profile)  
profile_blueprint.route('/profiles', methods=['GET'])(find_all)  
profile_blueprint.route('/profiles/<int:profile_id>', methods=['GET'])(find_by_id)  
profile_blueprint.route('/profiles/<int:profile_id>', methods=['PUT'])(update_profile_info)  
profile_blueprint.route('/profiles/<int:profile_id>', methods=['DELETE'])(delete_profile_info) 



