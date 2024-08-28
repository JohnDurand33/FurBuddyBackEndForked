from flask import request, jsonify
from models.schemas.taskSchema import task_schema, tasks_schema
from services.taskService import save_task, update_task, delete_task
from marshmallow import ValidationError

def save_task():
    try:
        task_data = task_schema.load(request.json)
        task_saved = save_task(task_data)
        return task_schema.jsonify(task_saved), 201
    except ValidationError as e:
        return jsonify(e.messages), 400

def update_task(id):
    try:
        task_data = request.json
        updated_task = update_task(id, task_data)
        if updated_task:
            return task_schema.jsonify(updated_task), 200
        else:
            return jsonify({"message": "Task not found"}), 404
    except ValidationError as e:
        return jsonify(e.messages), 400

def delete_task(id):
    try:
        success = delete_task(id)
        if success:
            return jsonify(success), 200
        else:
            return jsonify({"message": "Task not found"}), 404
    except ValidationError as e:
        return jsonify(e.messages), 400