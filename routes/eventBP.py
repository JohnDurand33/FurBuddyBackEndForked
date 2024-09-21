from flask import Blueprint
from controllers.eventControllers import create_event, get_event, get_events, update_event, delete_event

event_blueprint = Blueprint('event_bp', __name__)

event_blueprint.route('/', methods=['POST', 'OPTIONS'])(create_event)
event_blueprint.route('/<int:event_id>', methods=['GET', 'OPTIONS'])(get_event)
event_blueprint.route(
    '/<int:event_id>', methods=['PUT', 'OPTIONS'])(update_event)
event_blueprint.route(
    '/<int:event_id>', methods=['DELETE', 'OPTIONS'])(delete_event)
event_blueprint.route('/events', methods=['GET', 'OPTIONS'])(get_events)
