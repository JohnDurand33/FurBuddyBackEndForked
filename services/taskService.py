from models.task import Task
from database import db

def save(task_data):
    new_task = Task(title=task_data['title'], start_time=task_data['start_time'], end_time=task_data['end_time'])
    db.session.add(new_task)
    db.session.commit()
    db.session.refresh(new_task)
    return new_task


def find_all():
    return Task.query.all()


def update(task_id, task_data):
    task = Task.query.get(task_id)
    if not task:
        return None
    
    for key, value in task_data.items():
        setattr(task, key, value)
    
    db.session.commit()
    return task


def delete(task_id):
    task = Task.query.get(task_id)
    if not task:
        return None
    
    db.session.delete(task)
    db.session.commit()
    return True
