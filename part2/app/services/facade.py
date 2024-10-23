from app.models.review import Review  # Assuming Review model exists
from app.models.user import User  # Assuming User model exists
from app.models.place import Place  # Assuming Place model exists

class HBnBFacade:
    def create_review(self, review_data):
        # Validate if the user and place exist
        user = User.query.get(review_data['user_id'])
        place = Place.query.get(review_data['place_id'])
        
        if not user or not place:
            raise ValueError('User or Place not found')
        
        # Validate rating is within range (1-5)
        if not (1 <= review_data['rating'] <= 5):
            raise ValueError('Rating must be between 1 and 5')

        # Create a new review instance
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=review_data['user_id'],
            place_id=review_data['place_id']
        )
        review.save()  # Assuming save method commits the review to the database
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

        # Update review fields
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
        review.delete()  # Assuming delete method removes the review from the database
