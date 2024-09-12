from flask import Blueprint
from controllers.medicalRecordsControllers import add_medical_record, get_medical_record, edit_medical_record, delete_medical_record, get_categories, get_service_types, get_service_types_by_category
from controllers.medicalRecordsControllers import get_records_by_category, get_records_by_service_type, get_medical_records, get_paginated_medical_records

medical_record_blueprint = Blueprint('medical_record_db', __name__)


medical_record_blueprint.route('/', methods=['POST', 'OPTIONS'])(add_medical_record)
medical_record_blueprint.route('/<int:record_id>', methods=['GET', 'OPTIONS'])(get_medical_record)
medical_record_blueprint.route('/records', methods=['GET', 'OPTIONS'])(get_medical_records)
medical_record_blueprint.route('/paginated', methods=['GET', 'OPTIONS'])(get_paginated_medical_records)
medical_record_blueprint.route('/<int:record_id>', methods=['PUT', 'OPTIONS'])(edit_medical_record)
medical_record_blueprint.route('/<int:record_id>', methods=['DELETE', 'OPTIONS'])(delete_medical_record)


# Routes to help populate dropdowns
medical_record_blueprint.route('/categories', methods=['GET', 'OPTIONS'])(get_categories)
medical_record_blueprint.route('/service_types', methods=['GET', 'OPTIONS'])(get_service_types)
medical_record_blueprint.route('/service_types_by_category/<int:category_id>', methods=['GET', 'OPTIONS'])(get_service_types_by_category)

# Filters by category, by service type
medical_record_blueprint.route('/by_category/<int:category_id>', methods=['GET', 'OPTIONS'])(get_records_by_category)
medical_record_blueprint.route('/by_service_type/<int:service_type_id>', methods=['GET', 'OPTIONS'])(get_records_by_service_type)









