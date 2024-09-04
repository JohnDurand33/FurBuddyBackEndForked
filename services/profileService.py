from database import db
from datetime import datetime, date
from models.profile import Profile
from models.dogOwner import DogOwner
from models.schemas.profileSchema import profile_schema  
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from utils.util import handle_options


def calculate_age(date_of_birth):
    if date_of_birth is None:
        return None
    today = datetime.today().date()
    if isinstance(date_of_birth, datetime):
        date_of_birth = date_of_birth.date()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
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
    
    age = calculate_age(date_of_birth)
    profile_data['age'] = age
    
    new_profile = Profile(
        name=profile_data['name'],
        date_of_birth=date_of_birth,
        sex=profile_data['sex'],
        fixed=profile_data['fixed'],
        breed=profile_data['breed'],
        weight=profile_data['weight'],
        chip_number=profile_data['chip_number'],
        image_path=profile_data.get('image_path', None),
        vet_clinic_name=profile_data['vet_clinic_name', None],
        vet_clinic_phone=profile_data['vet_clinic_phone', None],
        vet_clinic_email=profile_data['vet_clinic_email', None],
        vet_doctor_name=profile_data['vet_doctor_name', None],
        owner_id=owner_id
        )
    
    try:
        db.session.add(new_profile)
        db.session.commit()
        db.session.refresh(new_profile)
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
        profiles = Profile.query.filter_by(owner_id).all()
        if not profiles:
            raise ValueError("No profiles found for the given owner.")
        return profiles
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









 