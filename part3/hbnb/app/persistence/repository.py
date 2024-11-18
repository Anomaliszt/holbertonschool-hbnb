from abc import ABC, abstractmethod

from app import db 
from app.models.user import User


class Repository(ABC):
    """
    Abstract base class for a repository.
    """

    @abstractmethod
    def add(self, obj):
        """
        Add an object to the repository.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Get an object from the repository by its ID.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Get all objects from the repository.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Get an object by a specific attribute.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Update an object in the repository.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Delete an object from the repository by its ID.
        """
        pass


class SQLAlchemyRepository(Repository):
    """
    SQLAlchemy implementation of the Repository.
    """

    def __init__(self, model):
        """
        Initialize the repository with the model to use.
        """
        self.model = model

    def add(self, obj):
        """
        Add an object to the database.
        """
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """
        Get an object from the database by its ID.
        """
        return self.model.query.get(obj_id)

    def get_all(self):
        """
        Get all objects from the database.
        """
        return self.model.query.all()

    def update(self, obj_id, **data):
        """
        Update an object in the database.
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """
        Delete an object from the database by its ID.
        """
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """
        Get an object from the database by a specific attribute.
        """
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
    
class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()