from flask import request, jsonify
from models.schemas.taskSchema import task_schema, tasks_schema
from services.taskService import save as save_event, find_all as find_all_tasks, update_task, delete_task
from marshmallow import ValidationError

def save():
    try:
        task_data = task_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    task_saved = save_event(task_data)
    return task_schema.jsonify(task_saved), 201

def find_all():
    all_events = find_all_tasks()
    return tasks_schema.jsonify(all_events), 200

def update(task_id):
    try:
        task_data = tasks_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    updated_task = update_task(task_id, task_data)
    if not updated_task:
        return jsonify({'message': 'Event not found'}), 404
    
    return task_schema.jsonify(updated_task), 200

def delete(task_id):
    deleted = delete_task(task_id)
    if not deleted:
        return jsonify({'message': 'Event not found'}), 404
    
    return '', 204
