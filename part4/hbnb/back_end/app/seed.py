from app import db, bcrypt
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
import uuid

def seed_database():
    """Seed the database with initial data"""
    if not User.query.filter_by(email='admin@hbnb.io').first():
        admin_password = bcrypt.generate_password_hash('admin1234').decode('utf-8')
        admin_user = User(
            id='36c9050e-ddd3-4c3b-9731-9f487208bbc1',
            email='admin@hbnb.io',
            first_name='Admin',
            last_name='HBnB',
            password=admin_password,
            is_admin=True
        )
        db.session.add(admin_user)

    amenities = [
        {'name': 'WiFi'},
        {'name': 'Swimming Pool'},
        {'name': 'Air Conditioning'}
    ]

    for amenity_data in amenities:
        if not Amenity.query.filter_by(name=amenity_data['name']).first():
            amenity = Amenity(name=amenity_data['name'])
            db.session.add(amenity)

    sample_place_id = str(uuid.uuid4())
    if not Place.query.filter_by(title='Cozy Downtown Apartment').first():
        sample_place = Place(
            id=sample_place_id,
            title='Cozy Downtown Apartment',
            description='A beautiful apartment in the heart of the city',
            price=100.00,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id='36c9050e-ddd3-4c3b-9731-9f487208bbc1'
        )
        db.session.add(sample_place)

        wifi = Amenity.query.filter_by(name='WiFi').first()
        ac = Amenity.query.filter_by(name='Air Conditioning').first()
        if wifi and ac:
            sample_place.amenities.extend([wifi, ac])

        sample_review = Review(
            id=str(uuid.uuid4()),
            text="Great location and very comfortable! Would definitely stay again.",
            rating=5,
            place_id=sample_place_id,
            user_id='36c9050e-ddd3-4c3b-9731-9f487208bbc1'
        )
        db.session.add(sample_review)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()