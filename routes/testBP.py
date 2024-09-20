from flask import Blueprint, jsonify

test_blueprint = Blueprint('test_bp', __name__)

@test_blueprint.route('/test-email', methods=['POST'])
def test_email():
    from services.emailReminder import send_email_reminder
    event_data = {
        "name": "Test Event",
        "start_time": "2024-09-19T17:00:00",
        "owner": {
            "owner_name": "Test Owner",
            "owner_email": "test@example.com"
        }
    }

    send_email_reminder(event_data['owner']['owner_email'], event_data)

    return jsonify({"message": "Test email sent!"}), 200