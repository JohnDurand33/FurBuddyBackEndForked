from database import db
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from models.event import Event 
from services.emailReminder import send_email_reminder
import logging


def check_for_upcoming_events():
    try:
        with sessionmaker(bind=db.engine)() as session:
            now = datetime.now()
            reminder_time = now + timedelta(hours=24)

            upcoming_events = session.query(Event).filter(
                Event.start_time <= reminder_time,
                Event.start_time > now
            ).all()

            for event in upcoming_events:
                try:
                    send_email_reminder(event.owner.owner_email, event)
                except Exception as e:
                    logging.error(f"Error sending email for event '{event.name}': {e}")

    except Exception as e:
        logging.error(f"Error checking for upcoming events: {e}")


def start_reminder_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_for_upcoming_events, 'interval', hours=1)
    scheduler.start()
    return scheduler

def shutdown_scheduler(scheduler):
    if scheduler is not None:
        scheduler.shutdown()
