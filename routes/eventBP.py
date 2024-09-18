from flask import Blueprint
from controllers.eventControllers import create_event, get_event, get_events, update_event, delete_event

event_blueprint = Blueprint('event_bp', __name__)

event_blueprint.route('/', methods=['POST'])(create_event)
event_blueprint.route('/<int:event_id>', methods=['GET'])(get_event)
event_blueprint.route('/<int:event_id>', methods=['PUT'])(update_event)
event_blueprint.route('/<int:event_id>', methods=['DELETE'])(delete_event)
event_blueprint.route('/events', methods=['GET'])(get_events)
