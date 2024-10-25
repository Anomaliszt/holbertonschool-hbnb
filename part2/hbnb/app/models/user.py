import re
from app.models.BaseModel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self.validate_name(first_name)
        self.last_name = self.validate_name(last_name)
        self.email = self.validate_email(email)
        self.is_admin = is_admin

    @staticmethod
    def validate_name(name):
        if not name or len(name) > 50:
            raise ValueError("Name must be provided and cannot exceed 50 characters.")
        return name

    @staticmethod
    def validate_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")
        return email