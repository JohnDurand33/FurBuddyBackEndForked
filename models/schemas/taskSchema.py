# from marshmallow import fields
# from database import ma

# class TaskSchema(ma.Schema):
#     id = fields.Integer(dump_only=True)
#     title = fields.String(required=True)
#     start_time = fields.DateTime(required=True, format='%Y-%m-%dT%H:%M:%S')
#     end_time = fields.DateTime(required=True, format='%Y-%m-%dT%H:%M:%S')
#     owner_email = fields.Email(required=True)

#     class Meta:
#         fields = ("id", "title", "start_time", "end_time", "owner_email")

# task_schema = TaskSchema()
# tasks_schema = TaskSchema(many=True)
