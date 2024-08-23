from models.schemas import ma
from marshmallow import fields

class ProfileSchema(ma.Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    age = fields.Integer()
    sex = fields.String()
    fixed = fields.Boolean()
    breed = fields.String()
    weight = fields.String()
    chip_number = fields.String()
    image_path = fields.String()
    vet = fields.String()
    vet_contact = fields.String()
  
    
    class Meta:
        fields = ("id", "name", "age", "sex", "fixed", "breed", "weight", "chip_number", "image_path", "vet", "vet_contact")
        
profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)
    
    