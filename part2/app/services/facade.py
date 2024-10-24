from app.models.review import Review
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.persistence.repository import Repository
from app.models.user import User
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def create_review(self, review_data):
        user = User.query.get(review_data['user_id'])
        place = Place.query.get(review_data['place_id'])
        
        if not user or not place:
            raise ValueError('User or Place not found')
        
        if not (1 <= review_data['rating'] <= 5):
            raise ValueError('Rating must be between 1 and 5')

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=review_data['user_id'],
            place_id=review_data['place_id']
        )
        review.save()
        return review

    def get_review(self, review_id):
        review = Review.query.get(review_id)
        if not review:
            raise ValueError('Review not found')
        return review

    def get_all_reviews(self):
        return Review.query.all()

    def get_reviews_by_place(self, place_id):
        place = Place.query.get(place_id)
        if not place:
            raise ValueError('Place not found')
        return Review.query.filter_by(place_id=place_id).all()

    def update_review(self, review_id, review_data):
        review = Review.query.get(review_id)
        if not review:
            raise ValueError('Review not found')

        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data and 1 <= review_data['rating'] <= 5:
            review.rating = review_data['rating']

        review.save()
        return review

    def delete_review(self, review_id):
        review = Review.query.get(review_id)
        if not review:
            raise ValueError('Review not found')
        review.delete()


class HBnBFacade:
    def __init__(self):
        self.amenity_repository = Repository()

    def create_amenity(self, amenity_data):
        """Create a new amenity with the given data."""
        if 'name' not in amenity_data or not amenity_data['name']:
            raise ValueError("Amenity name is required")
        
        new_amenity = Amenity(name=amenity_data['name'])
        return self.amenity_repository.save(new_amenity)

    def get_amenity(self, amenity_id):
        """Retrieve a specific amenity by its ID."""
        amenity = self.amenity_repository.get_by_id(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        return amenity

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity by its ID."""
        amenity = self.amenity_repository.get_by_id(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        
        return self.amenity_repository.save(amenity)


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
    
    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass

    def create_place(self, place_data):
        # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        pass

    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        pass

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        pass

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        pass