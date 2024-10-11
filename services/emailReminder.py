from flask_mail import Message
from flask import current_app

def send_email_reminder(owner_email, event):
    from app import mail  

    msg = Message(
        subject=f"Reminder: {event.name} is coming up!",
        recipients=[owner_email],
        body=f"Dear {event.owner.owner_name},\n\n"
             f"This is a reminder that your event '{event.name}' is scheduled for {event.start_time}.\n"
             f"Location: {event.street}, {event.state} {event.zip_code}\n\n"
             f"Notes: {event.notes}\n\n"
    )
    
    with current_app.app_context():
        mail.send(msg)