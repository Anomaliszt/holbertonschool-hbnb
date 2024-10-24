from app.models.BaseModel import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place_id = place_id
        self.user_id = user_id

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