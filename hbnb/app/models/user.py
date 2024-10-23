import re
from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required and must be 50 characters or less")
        
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and must be 50 characters or less")
        
        if not email or not re.match(self.EMAIL_REGEX, email):
            raise ValueError("A valid email address is required")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
