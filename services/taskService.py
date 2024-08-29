# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from celery import Celery
# from datetime import datetime, timedelta
# from models.task import db, Task
# from models.schemas.taskSchema import task_schema  


# def save_task(task_data):
#     try:
#         new_event = Task(
#             title=task_data['title'],  
#             start_time=datetime.fromisoformat(task_data['start_time']),
#             end_time=datetime.fromisoformat(task_data['end_time']),
#             user_email=task_data['user_email']
#         )
#         db.session.add(new_event)
#         db.session.commit()
#         db.session.refresh(new_event)
        
#         reminder_time = new_event.start_time - timedelta(hours=24)
#         send_reminder.apply_async((new_event.owner_email, new_event.title), eta=reminder_time)  
        
#         return new_event
#     except Exception as e:
#         db.session.rollback()
#         raise e

# def update_task(task_id, task_data):
#     try:
#         task = db.session.query(Task).filter(Task.id == task_id).first()
#         if task:
#             for key, value in task_data.items():
#                 setattr(task, key, value)
#             db.session.commit()
#             db.session.refresh(task)
#             return task
#         else:
#             return None
#     except Exception as e:
#         db.session.rollback()
#         raise e

# def delete_task(task_id):
#     try:
#         task = db.session.query(Task).filter(Task.id == task_id).first()
#         if task:
#             db.session.delete(task)
#             db.session.commit()
#             return {'message': 'Task deleted successfully'}
#         else:
#             return None
#     except Exception as e:
#         db.session.rollback()
#         raise e
    

