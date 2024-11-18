from app.models.BaseModel import BaseModel
from app import bcrypt, db

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    @staticmethod
    def validate_text(text):
        if not text:
            raise ValueError("Review text must be provided.")
        return text

    @staticmethod
    def validate_rating(rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return rating