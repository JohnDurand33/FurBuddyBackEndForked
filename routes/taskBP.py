from flask import Blueprint
from controllers.taskControllers import save_task, update_task, delete_task

task_blueprint = Blueprint('task_bp', __name__)

task_blueprint.route('/', methods=['POST'])(save_task)
task_blueprint.route('/<int:task_id>', methods=['PUT'])(update_task)
task_blueprint.route('/<int:task_id>', methods=['DELETE'])(delete_task)
