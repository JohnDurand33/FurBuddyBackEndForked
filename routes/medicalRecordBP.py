from flask import Blueprint
from controllers.medicalRecordsControllers import add_medical_record, get_medical_record, edit_medical_record, add_medical_record, delete_medical_record
from controllers.medicalRecordsControllers import get_paginated_medical_records, filter_records_by_category, filter_records_by_service_type, get_service_types_by_category

medical_record_blueprint = Blueprint('medical_record_db', __name__)

# Fully functional and ready to be used
medical_record_blueprint.route('/', methods=['POST', 'OPTIONS'])(add_medical_record)
medical_record_blueprint.route('/<int:record_id>', methods=['GET', 'OPTIONS'])(get_medical_record)
medical_record_blueprint.route('/<int:record_id>', methods=['PUT', 'OPTIONS'])(edit_medical_record)
medical_record_blueprint.route('/<int:record_id>', methods=['DELETE', 'OPTIONS'])(delete_medical_record)


# This enpoint could help to populate dropdowns with service types based on the selected categoryif you want to use it.
# But I tied particulat category to service type already in DB according to Alice's list.
service_type_by_category_blueprint = Blueprint('service_type_by_category_db', __name__)
service_type_by_category_blueprint.route('/service_types_by_category/<int:category_id>', methods=['GET', 'OPTIONS'])(get_service_types_by_category)


# Still working on those, not ready
medical_record_blueprint.route('/records', methods=['GET', 'OPTIONS'])(get_paginated_medical_records)
medical_record_blueprint.route('/category/<int:category_id>', methods=['GET', 'OPTIONS'])(filter_records_by_category)
medical_record_blueprint.route('/service_type/<int:service_type_id>', methods=['GET', 'OPTIONS'])(filter_records_by_service_type)



