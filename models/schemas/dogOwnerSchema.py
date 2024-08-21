from models.schemas import ma
from marshmallow import fields

class DogOwnerSchema(ma.Schema):
    id = fields.Integer(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    owner_name = fields.String(required=True)
    owner_email = fields.String(required=True)
    owner_phone = fields.String()

    class Meta:
        fields = ("id", "username", "password", "owner_name", "owner_email", "owner_phone" )
        
dog_owner_schema = DogOwnerSchema()
dog_owners_schema = DogOwnerSchema(many=True)