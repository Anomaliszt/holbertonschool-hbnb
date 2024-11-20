import re
from app.models.BaseModel import BaseModel
from app import bcrypt, db


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    @classmethod
    def create_user(cls, first_name, last_name, email, password, is_admin=False):
        first_name = cls.validate_name(first_name, "First")
        last_name = cls.validate_name(last_name, "Last")
        email = cls.validate_email(email)
        hashed_password = cls.hash_password(password)
        return cls(first_name=first_name, last_name=last_name, email=email, password=hashed_password, is_admin=is_admin)

    @staticmethod
    def validate_name(name, field_name):
        if not name or len(name) > 50:
            raise ValueError("{} name must be provided and cannot exceed 50 characters.".format(field_name))
        return name

    @staticmethod
    def validate_email(email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.fullmatch(regex, email):
            raise ValueError("Invalid email format")
        return email
    
    @staticmethod
    def hash_password(password):
        """Hashes the password before storing it."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)