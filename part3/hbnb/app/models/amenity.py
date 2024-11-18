from app.models.BaseModel import BaseModel
from app import bcrypt, db

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    @staticmethod
    def validate_name(name):
        if not name or len(name) > 50:
            raise ValueError("Amenity name must be provided and cannot exceed 50 characters.")
        return name