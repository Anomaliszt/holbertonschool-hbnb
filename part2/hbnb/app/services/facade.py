from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, updated_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(updated_data)
        self.user_repo.update(user_id, updated_data)
        return user

    def create_amenity(self, amenity_data):
        if 'name' not in amenity_data or not amenity_data['name']:
            raise ValueError("Amenity name is required.")
        
        new_amenity = Amenity(n**amenity_data)
        self.amenity_repo.add(new_amenity)
        return new_amenity.id

    def get_amenity(self, amenity_id):
        """retrieve an amenity by its ID"""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity is None:
            raise LookupError("Amenity not found")
        return amenity

    def get_all_amenities(self):
        """retrieve all amnities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity by its ID."""
        existing_amenity = self.amenity_repo.get(amenity_id)
        if existing_amenity is None:
            raise LookupError("Amenity not found")

        if 'name' in amenity_data:
            existing_amenity.name = amenity_data['name']

        self.amenity_repo.update(existing_amenity)
        return existing_amenity

    def create_place(self, place_data):
        new_place = Place(**place_data)
        self.place_repo.add(new_place)
        return new_place   

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place is None:
            raise LookupError("Place not found.")
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        existing_place = self.place_repo.get(place_id)
