# from celery import Celery
# from flask_mail import Message
# from app import create_app, mail
# from models.task import Task
# from datetime import datetime, timedelta

# app = create_app()
# celery = Celery(
#     app.import_name,
#     backend=app.config['CELERY_RESULT_BACKEND'],
#     broker=app.config['CELERY_BROKER_URL']
# )
# celery.conf.update(app.config)

# @celery.task
# def send_email_reminder(task_id):
#     with app.app_context():
#         task = Task.query.get(task_id)
#         if not task:
#             return

#         msg = Message(
#             subject='Reminder: Upcoming Task',
#             sender=app.config['MAIL_USERNAME'],
#             recipients=['recipient-email@example.com'],
#             body=f'Reminder: The tesk "{task.title}" is scheduled for {task.start_time}.'
#         )
#         mail.send(msg)

# def schedule_reminders():
#     now = datetime.now()
#     future_events = Task.query.filter(Task.start_time <= now + timedelta(days=1)).all()
    
#     for task in future_events:
#         send_email_reminder.apply_async(args=[task.id], eta=task.start_time - timedelta(hours=24))
