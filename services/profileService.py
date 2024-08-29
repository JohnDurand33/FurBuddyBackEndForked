from database import db
from datetime import datetime
from models.profile import Profile
from models.dogOwner import DogOwner
from models.schemas.profileSchema import profile_schema  
from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from utils.util import token_required


def calculate_age(date_of_birth):
    if date_of_birth is None:
        return None
    today = datetime.today().date()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return age


def save(profile_data, owner_id):
  
    owner = db.session.get(DogOwner, owner_id)
    if not owner:
        raise ValueError(f"Owner with ID {owner_id} does not exist.")
    
    date_of_birth = profile_data.get('date_of_birth')
    if date_of_birth:
        try:
            date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Date of birth must be in YYYY-MM-DD format.")
    else:
        date_of_birth = None
    
    new_profile = Profile(
        name=profile_data['name'],
        date_of_birth=date_of_birth,
        sex=profile_data['sex'],
        fixed=profile_data['fixed'],
        breed=profile_data['breed'],
        weight=profile_data['weight'],
        chip_number=profile_data['chip_number'],
        image_path=profile_data.get('image_path', None),
        vet_clinic_name=profile_data['vet_clinic_name'],
        vet_clinic_phone=profile_data['vet_clinic_phone'],
        vet_clinic_email=profile_data['vet_clinic_email'],
        vet_doctor_name=profile_data['vet_doctor_name'],
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
        
        
@token_required
def get_profile_with_owner(profile_id, current_owner_id):
    
    profile_query = select(Profile).where(Profile.id == profile_id, Profile.owner_id == current_owner_id)
    profile_result = db.session.execute(profile_query).scalars().one_or_none()
    
    if profile_result is None:
        raise NoResultFound(f'Profile with ID {profile_id} not found or you do not own this profile.')

    owner_query = select(DogOwner).where(DogOwner.id == current_owner_id)
    owner_result = db.session.execute(owner_query).scalars().one_or_none()
    
    if owner_result is None:
        raise NoResultFound(f'Owner with ID {current_owner_id} not found.')

    return {
        'profile': profile_result,
        'owner': owner_result
    }


@token_required
def find_all(current_owner_id):
    query = select(Profile).where(Profile.owner_id == current_owner_id)
    all_profiles = db.session.execute(query).scalars().all()
    return all_profiles


@token_required
def find_by_id(profile_id, current_owner_id):
        query = select(Profile).where(Profile.id == profile_id, Profile.owner_id == current_owner_id)
        result = db.session.execute(query).scalars().one_or_none()
        
        if result is None:
            raise NoResultFound(f'Profile with ID {profile_id} not found or you do not own this profile.')
       
        age = calculate_age(result.date_of_birth)
        
        profile_data = profile_schema.dump(result)
        profile_data['age'] = age
        
        return profile_data
    

@token_required
def update_profile(profile_id, profile_data, current_owner_id):
    
    query = select(Profile).where(Profile.id == profile_id, Profile.owner_id == current_owner_id)
    result = db.session.execute(query).scalars().one_or_none()
    
    if result is None:
        raise NoResultFound(f'Profile with ID {profile_id} not found or you do not own this profile.')

    for key, value in profile_data.items():
        setattr(result, key, value)
    
    try:
        db.session.commit()
        return result
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Database Integrity Error: {e}")
  
  
@token_required
def delete_profile(profile_id, current_owner_id):
    query = select(Profile).where(Profile.id == profile_id, Profile.owner_id == current_owner_id)
    profile = db.session.execute(query).scalars().one_or_none()
    
    if profile is None:
        raise NoResultFound(f'Profile with ID {profile_id} not found or you do not own this profile.')

    query = delete(Profile).where(Profile.id == profile_id)
    result = db.session.execute(query)
    
    try:
        db.session.commit()
        if result.rowcount == 0:
            raise NoResultFound(f'Profile with ID {profile_id} not found.')
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Database Integrity Error: {e}")
    
    return {"status": "success", "message": "Profile deleted successfully"}
    
 