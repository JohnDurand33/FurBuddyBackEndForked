from database import db
from datetime import datetime, date
from models.profile import Profile
from models.dogOwner import DogOwner
from models.schemas.profileSchema import profile_schema  
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from utils.util import handle_options


def calculate_age(date_of_birth):
    if date_of_birth is None:
        return None
    today = datetime.today().date()
    if isinstance(date_of_birth, datetime):
        date_of_birth = date_of_birth.date()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    print(f"Date of Birth: {date_of_birth}, Today: {today}, Calculated Age: {age}")
    return age


def save(profile_data, owner_id):
  
    owner = db.session.get(DogOwner, owner_id)
    if not owner:
        raise ValueError(f"Owner with ID {owner_id} does not exist.")
    
    date_of_birth = profile_data.get('date_of_birth', None)
    
    if isinstance(date_of_birth, str):
        try:
            date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Date of birth must be in YYYY-MM-DD format.")
    elif date_of_birth is not None and not isinstance(date_of_birth, (date, datetime)):
        raise ValueError("Date of birth must be a string or a date object.")
    
    # age = calculate_age(date_of_birth)
    # profile_data['age'] = age
    # print(f"Calculated Age: {age}")
    
    new_profile = Profile(
        name=profile_data['name'],
        date_of_birth=date_of_birth,
        sex=profile_data['sex'],
        fixed=profile_data['fixed'],
        breed=profile_data['breed'],
        weight=profile_data['weight'],
        chip_number=profile_data['chip_number'],
        image_path=profile_data.get('image_path', None),
        vet_clinic_name=profile_data.get('vet_clinic_name', None),
        vet_clinic_phone=profile_data.get('vet_clinic_phone', None),
        vet_clinic_email=profile_data.get('vet_clinic_email', None),
        vet_doctor_name=profile_data.get('vet_doctor_name', None),
        owner_id=owner_id
        )
    
    try:
        db.session.add(new_profile)
        db.session.commit()
        db.session.refresh(new_profile)
        
        age = calculate_age(new_profile.date_of_birth)

        new_profile = {
            'id': new_profile.id,
            'name': new_profile.name,
            'date_of_birth': new_profile.date_of_birth.isoformat() if new_profile.date_of_birth else None,
            'age': age,
            'sex': new_profile.sex,
            'fixed': new_profile.fixed,
            'breed': new_profile.breed,
            'weight': new_profile.weight,
            'chip_number': new_profile.chip_number,
            'image_path': new_profile.image_path,
            'vet_clinic_name': new_profile.vet_clinic_name,
            'vet_clinic_phone': new_profile.vet_clinic_phone,
            'vet_clinic_email': new_profile.vet_clinic_email,
            'vet_doctor_name': new_profile.vet_doctor_name,
            'owner_id': new_profile.owner_id
        }

        return new_profile

    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Database Integrity Error: {e}")
        
        
        
def find_profile_by_id(profile_id):
    profile = db.session.get(Profile, profile_id)
    if not profile:
        raise ValueError(f"Profile with ID {profile_id} does not exist.")
    return profile
        
        
def find_all_profiles(owner_id):
    try:
        profiles = db.session.query(Profile).filter(Profile.owner_id == owner_id).all()
        if not profiles:
            raise ValueError("No profiles found for the given owner.")
        
        result = []
        for profile in profiles:
            profile_data = {
                'id': profile.id,
                'name': profile.name,
                'date_of_birth': profile.date_of_birth.isoformat() if profile.date_of_birth else None,
                'age': calculate_age(profile.date_of_birth),
                'sex': profile.sex,
                'fixed': profile.fixed,
                'breed': profile.breed,
                'weight': profile.weight,
                'chip_number': profile.chip_number,
                'image_path': profile.image_path,
                'vet_clinic_name': profile.vet_clinic_name,
                'vet_clinic_phone': profile.vet_clinic_phone,
                'vet_clinic_email': profile.vet_clinic_email,
                'vet_doctor_name': profile.vet_doctor_name,
                'owner_id': profile.owner_id
            }
            result.append(profile_data)
        return result
    
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error retrieving profiles: {str(e)}")


def update_profile(profile_id, profile_data):
    profile = db.session.get(Profile, profile_id)
    if not profile:
        raise ValueError(f"Profile with ID {profile_id} does not exist.")
    
    for key, value in profile_data.items():
        setattr(profile, key, value)
    
    try:
        db.session.commit()
        db.session.refresh(profile)
        return profile
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Database Integrity Error: {e}")
     
     
def delete_profile(profile_id):
    profile = db.session.get(Profile, profile_id)
    if not profile:
        raise ValueError(f"Profile with ID {profile_id} does not exist.")
    
    try:
        db.session.delete(profile)
        db.session.commit()
        return True
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Database Integrity Error: {e}")









 