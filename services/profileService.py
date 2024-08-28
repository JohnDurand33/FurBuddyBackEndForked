from database import db
from models.profile import Profile
from models.dogOwner import DogOwner
from services import dogOwnerService  
from models.schemas.profileSchema import profile_schema  
from models.schemas.dogOwnerSchema import dog_owner_schema
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
# from gcd_service import upload_image, delete_image

def save(profile_data, owner_id):
    
    # if image_file:
    #     image_path = upload_image(image_file, image_file.filename)
    #     profile_data['image_path'] = image_path
    
    owner = db.session.get(DogOwner, owner_id)
    if not owner:
        raise ValueError(f"Owner with ID {owner_id} does not exist.")
    
    
    new_profile = Profile(
        name=profile_data['name'],
        age=profile_data['age'],
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
        
        
def get_profile_with_owner(profile_id, owner_id):
    
    profile_query = select(Profile).where(Profile.id == profile_id, Profile.owner_id == owner_id)
    profile_result = db.session.execute(profile_query).scalars().one_or_none()
    
    if profile_result is None:
        raise NoResultFound(f'Profile with ID {profile_id} not found or you do not own this profile.')

    owner_query = select(DogOwner).where(DogOwner.id == owner_id)
    owner_result = db.session.execute(owner_query).scalars().one_or_none()
    
    if owner_result is None:
        raise NoResultFound(f'Owner with ID {owner_id} not found.')

    return {
        'profile': profile_result,
        'owner': owner_result
    }


def find_all(owner_id):
    query = select(Profile).where(Profile.owner_id == owner_id)
    all_profiles = db.session.execute(query).scalars().all()
    return all_profiles


def find_by_id(profile_id, owner_id):
    query = select(Profile).where(Profile.id == profile_id, Profile.owner_id == owner_id)
    result = db.session.execute(query).scalars().one_or_none()
    if result is None:
        raise NoResultFound(f'Profile with ID {profile_id} not found or you do not own this profile.')
    return result


def update_profile(profile_id, profile_data, owner_id):
    # Fetch the profile
    query = select(Profile).where(Profile.id == profile_id, Profile.owner_id == owner_id)
    result = db.session.execute(query).scalars().one_or_none()
    
    if result is None:
        raise NoResultFound(f'Profile with ID {profile_id} not found or you do not own this profile.')

    # Update the profile
    for key, value in profile_data.items():
        setattr(result, key, value)
    
    try:
        db.session.commit()
        return result
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Database Integrity Error: {e}")
    
    
    # if image_file:
    #     if profile.image_path:
    #         delete_image(profile.image_path.split('/')[-1])
    #     image_path = upload_image(image_file, image_file.filename)
    #     profile_data['image_path'] = image_path
    
  

def delete_profile(profile_id, owner_id):
    query = select(Profile).where(Profile.id == profile_id, Profile.owner_id == owner_id)
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
    
    
    # if profile.image_path:
    #     delete_image(profile.image_path.split('/')[-1])
        
  