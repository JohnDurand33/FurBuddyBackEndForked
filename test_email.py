import pytest
from flask import Flask
from services.emailReminder import send_email_reminder
from models.event import Event
from models.dogOwner import DogOwner 
from database import db
from app import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()  
    with app.app_context():
       
        db.create_all()  
        yield app
        db.session.remove()  
        db.drop_all()  


@pytest.fixture
def dog_owner(app):
    """Create a DogOwner instance for testing."""
    owner = DogOwner(
        owner_name="Test Owner",
        owner_email="test@example.com",
        password="testpassword"
    )
    db.session.add(owner)
    db.session.commit()
    return owner

@pytest.fixture
def event_data(dog_owner):
    """Return event data including a valid owner."""
    return {
        "name": "Test Event",
        "start_time": "2024-09-19T17:00:00",
        "owner": {
            "owner_name": dog_owner.owner_name,
            "owner_email": dog_owner.owner_email
        }
    }

def test_send_email_reminder(mocker, app, event_data, dog_owner):
    """Test the send_email_reminder function."""
   
    mock_send = mocker.patch('flask_mail.Mail.send')

    event = Event(
        name=event_data['name'],
        street=None,  
        zip_code=None, 
        state=None, 
        start_time=event_data['start_time'],
        end_time=event_data['start_time'],  
        notes=None,  
        owner_id=dog_owner.id  
    )
  
    db.session.add(event)
    db.session.commit()

    send_email_reminder(event_data['owner']['owner_email'], event)

    mock_send.assert_called_once()