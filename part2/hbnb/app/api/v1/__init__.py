# api/__init__.py

from flask_restx import Api
from flask import Blueprint
from api.v1.amenities import api as amenities_ns  # Import the amenities namespace

# Create a blueprint for your API
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

# Create an instance of the API with the blueprint
api = Api(
    blueprint,
    title='HBnB API',  # Title of your API documentation
    version='1.0',  # Version of your API
    description='API for managing HBnB application'  # Brief description
)

# Register the amenities namespace with the API
api.add_namespace(amenities_ns)

# The blueprint needs to be registered with your main Flask app elsewhere in the project
