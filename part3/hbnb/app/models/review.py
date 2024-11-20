from app.models.BaseModel import BaseModel
from app import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    @classmethod
    def create(cls, text, rating, place_id, user_id):
        validated_text = cls.validate_text(text)
        validated_rating = cls.validate_rating(rating)
        return cls(text=validated_text, rating=validated_rating, place_id=place_id, user_id=user_id)

    @staticmethod
    def validate_text(text):
        if text == "":
            raise ValueError("Review text must be provided.")
        return text

    @staticmethod
    def validate_rating(rating):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        return rating
