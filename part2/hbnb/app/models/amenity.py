from app.models.BaseModel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = self.validate_name(name)

    @staticmethod
    def validate_name(name):
        if not name or len(name) > 50:
            raise ValueError("Amenity name must be provided and cannot exceed 50 characters.")
        return name