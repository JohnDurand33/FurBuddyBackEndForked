# from flask import Blueprint, request, jsonify
# from services.eventService import create_event, get_event, update_event, delete_event, get_all_events
# from utils.util import token_required, handle_options


# @handle_options
# @token_required
# def create_event(current_owner_id):
#     data = request.get_json()
#     try:
#         result = create_event(current_owner_id, data)
#         return jsonify(result), 201
#     except Exception as e:
#         return jsonify({"message": str(e)}), 400


# @handle_options
# @token_required
# def get_event(current_owner_id, event_id):
#     result = get_event(current_owner_id, event_id)
#     if result is None:
#         return jsonify({"message": "Unauthorized"}), 403
#     return jsonify(result)


# @handle_options
# @token_required
# def update_event(current_owner_id, event_id):
#     data = request.get_json()
#     result = update_event(current_owner_id, event_id, data)
#     if result is None:
#         return jsonify({"message": "Unauthorized"}), 403
#     return jsonify(result)


# @handle_options
# @token_required
# def delete_event(current_owner_id, event_id):
#     result = delete_event(current_owner_id, event_id)
#     if result is None:
#         return jsonify({"message": "Unauthorized"}), 403
#     return jsonify(result), 200


# @handle_options
# @token_required
# def get_events(current_owner_id):
#     view_type = request.args.get('view')  
#     start_date_str = request.args.get('start_date')
#     year = request.args.get('year')
#     month = request.args.get('month')

#     try:
#         events = get_all_events(view_type, start_date_str, year, month, current_owner_id)
#         return jsonify(events)
#     except ValueError as e:
#         return jsonify({"message": str(e)}), 400
#     except Exception as e:
#         return jsonify({"message": "An error occurred: " + str(e)}), 500
