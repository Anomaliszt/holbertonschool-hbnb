from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
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
            raise ValueError("Amenity name is required")
        
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by its ID"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        return amenity

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity by its ID."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        
        self.amenity_repo.add(amenity)
        return amenity

    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        place.update(place_data)
        self.place_repo.update(place_id, place_data)
        return place

    def create_review(self, review_data):
        new_review = Review(**review_data)
        self.review_repo.add(new_review)
        return new_review

    def get_all_reviews(self):
        return self.review_repo.get_all()
    
    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError('Place not found')
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]


    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError('Review not found')

        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data and 1 <= review_data['rating'] <= 5:
            review.rating = review_data['rating']

        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError('Review not found')
        self.review_repo.delete(review_id)
