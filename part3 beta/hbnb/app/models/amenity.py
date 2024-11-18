from app.models.BaseModel import BaseModel
from app import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    _name = db.Column(db.String(128), nullable=False)

    @classmethod
    def create(cls, name):
        validated_name = cls.validate_name(name)
        return cls(name=validated_name)

    @staticmethod
    def validate_name(name):
        if not name or len(name) > 50:
            raise ValueError("Amenity name must be provided and cannot exceed 50 characters.")
        return name