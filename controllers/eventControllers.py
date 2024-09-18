from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from services.eventService import create_new_event, get_event_by_id, update_event_by_id, delete_event_by_id, get_all_events
from utils.util import token_required, handle_options


@handle_options
@token_required
def create_event(current_owner_id):
    data = request.get_json()
    try:
        result = create_new_event(current_owner_id, data)
        return jsonify(result), 201
    except ValidationError as err:
        return jsonify({"message": err.messages}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@handle_options
@token_required
def get_event(current_owner_id, event_id):
    result = get_event_by_id(current_owner_id, event_id)
    if result is None:
        return jsonify({"message": "Event not found"}), 404
    return jsonify(result)


@handle_options
@token_required
def update_event(current_owner_id, event_id):
    data = request.get_json()
    result = update_event_by_id(current_owner_id, event_id, data)
    if result is None:
        return jsonify({"message": "Event not found"}), 404
    return jsonify(result)


@handle_options
@token_required
def delete_event(current_owner_id, event_id):
    result = delete_event_by_id(current_owner_id, event_id)
    if result is None:
        return jsonify({"message": "Event not found"}), 404
    return jsonify(result), 200


@handle_options
@token_required
def get_events(current_owner_id):
    view_type = request.args.get('view')  
    start_date_str = request.args.get('start_date')
    year = request.args.get('year')
    month = request.args.get('month')

    try:
        events = get_all_events(view_type, start_date_str, year, month, current_owner_id)
        return jsonify(events)
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500
