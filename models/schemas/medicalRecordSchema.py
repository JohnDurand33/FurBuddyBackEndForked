from models.schemas import ma
from marshmallow import fields, Schema



class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    category_name = fields.Str(required=True)

    class Meta:
        fields = ("id", "category_name")
        
category_schema = CategorySchema()
        
        
        
class ServiceTypeSchema(Schema):
    id = fields.Int(dump_only=True)
    service_type_name = fields.Str(required=True)


    class Meta:
        fields = ("id", "service_type_name")
        
service_type_schema = ServiceTypeSchema()
        


class MedicalRecordSchema(Schema):
    id = fields.Integer(dump_only=True)
    service_date = fields.Date(required=True)
    category_id = fields.Integer(required=True)
    service_type_id = fields.Integer(required=True)
    follow_up_date = fields.Date(allow_none=True)
    fee = fields.Decimal(as_string=True, allow_none=True)
    image_path = fields.String(allow_none=True)
    profile_id = fields.Integer(required=True)

    category = fields.Nested('CategorySchema', dump_only=True)
    service_type = fields.Nested('ServiceTypeSchema', dump_only=True)

    class Meta:
        fields = (
            "id", "service_date", "category_id", "service_type_id", 
            "follow_up_date", "fee", "image_path", "profile_id", 
            "category", "service_type"
        )
        
medical_record_schema = MedicalRecordSchema()
medical_records_schema = MedicalRecordSchema(many=True)


       