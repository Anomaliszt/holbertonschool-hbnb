from app.models.BaseModel import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []

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