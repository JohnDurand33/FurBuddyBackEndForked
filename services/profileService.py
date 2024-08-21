from database import db
from models.profile import Profile
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
# from gcd_service import upload_image, delete_image

def save(profile_data):
    
    # if image_file:
    #     image_path = upload_image(image_file, image_file.filename)
    #     profile_data['image_path'] = image_path
    
    new_profile = Profile(
        name=profile_data['name'],
        age=profile_data['age'],
        sex=profile_data['sex'],
        fixed=profile_data['fixed'],
        breed=profile_data['breed'],
        weight=profile_data['weight'],
        chip_number=profile_data['chip_number'],
        image_path=profile_data['image_path']
        )
    
    db.session.add(new_profile)
    db.session.commit()
    db.session.refresh(new_profile)
    return new_profile


def find_all():
    query = select(Profile)
    all_profiles = db.session.execute(query).scalars().all()
    return all_profiles


def find_by_id(profile_id):
    query = select(Profile).filter(Profile.id == profile_id)
    result = db.session.execute(query).scalars().one_or_none()
    if result is None:
        raise NoResultFound(f'Profile with ID {profile_id} not found.')
    return result


def update(profile_id, profile_data):
    
    profile = find_by_id(profile_id)
    # if image_file:
    #     if profile.image_path:
    #         delete_image(profile.image_path.split('/')[-1])
    #     image_path = upload_image(image_file, image_file.filename)
    #     profile_data['image_path'] = image_path
        
    query = update(Profile).where(Profile.id == profile_id).values(profile_data)
    result = db.session.execute(query)
    db.session.commit()
    if result.rowcount == 0:
        raise NoResultFound(f'Profile with ID {profile_id} not found.')
    return find_by_id(profile_id)


def delete(profile_id):
    
    profile = find_by_id(profile_id)
    # if profile.image_path:
    #     delete_image(profile.image_path.split('/')[-1])
        
    query = delete(Profile).where(Profile.id == profile_id)
    result = db.session.execute(query)
    db.session.commit()
    if result.rowcount == 0:
        raise NoResultFound(f'Profile with ID {profile_id} not found.')