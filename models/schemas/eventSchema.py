import marshmallow as ma
from marshmallow import Schema, fields

class EventSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    street = fields.String(allow_none=True)
    zip_code = fields.String(allow_none=True)
    state = fields.String(allow_none=True)
    start_time = fields.DateTime(format='%Y-%m-%dT%H:%M:%S', required=True)
    end_time = fields.DateTime(format='%Y-%m-%dT%H:%M:%S', required=True)
    notes = fields.String(allow_none=True)
    

    class Meta:
        fields = ("id", "name", "street", "zip_code", "state", "start_time", "end_time", "notes")
        
event_schema = EventSchema()
events_schema = EventSchema(many=True)