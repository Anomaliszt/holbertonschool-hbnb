from app.models.BaseModel import BaseModel
from app import bcrypt, db

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    @staticmethod
    def validate_title(title):
        if not title or len(title) > 100:
            raise ValueError("Title must be provided and cannot exceed 100 characters.")
        return title

    @staticmethod
    def validate_price(price):
        if price <= 0:
            raise ValueError("Price must be a positive value.")
        return price

    @staticmethod
    def validate_latitude(latitude):
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        return latitude

    @staticmethod
    def validate_longitude(longitude):
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        return longitude

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)