from marshmallow import fields
from database import ma

class TaskSchema(ma.Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)

    class Meta:
        fields = ("id", "title", "start_time", "end_time")

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
