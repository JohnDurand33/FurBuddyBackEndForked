from models.schemas import ma
from marshmallow import fields

class ProfileSchema(ma.Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)
    date_of_birth = fields.Date(format='%Y-%m-%d', allow_none=True)
    age = fields.Integer(dump_only=True)
    sex = fields.String()
    fixed = fields.Boolean()
    breed = fields.String()
    weight = fields.String()
    chip_number = fields.String()
    image_path = fields.String()
    vet_clinic_name = fields.String()
    vet_clinic_phone = fields.String()
    vet_clinic_email = fields.String()
    vet_doctor_name = fields.String()
  
    class Meta:
        fields = ("id", "name", "date_of_birth", "age", "sex", "fixed", "breed", "weight", "chip_number", "image_path", "vet_clinic_name", "vet_clinic_phone", "vet_clinic_email", "vet_doctor_name")
        
profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)
    


