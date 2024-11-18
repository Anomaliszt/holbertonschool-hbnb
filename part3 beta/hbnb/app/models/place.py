from app.models.BaseModel import BaseModel
from app import db

class Place(BaseModel):
    __tablename__ = 'places'

    _title = db.Column(db.String(255), nullable=False)
    _description = db.Column(db.Text, nullable=True)
    _price = db.Column(db.Numeric(10, 2), nullable=False)
    _latitude = db.Column(db.Float, nullable=False)
    _longitude = db.Column(db.Float, nullable=False)
    _owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)


    @classmethod
    def create(cls, title, description, price, latitude, longitude, owner_id):
        title = cls.validate_title(title)
        price = cls.validate_price(price)
        latitude = cls.validate_latitude(latitude)
        longitude = cls.validate_longitude(longitude)
        instance = cls()
        instance._title = title
        instance._description = description
        instance._price = price
        instance._latitude = latitude
        instance._longitude = longitude
        instance._owner_id = owner_id
        instance.reviews = []
        instance.amenities = []
        return instance

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