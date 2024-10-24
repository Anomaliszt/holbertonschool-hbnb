from flask import Flask
from flask_restx import Api
from .api.v1.users import api as users_ns  # Note the leading dot
from .api.v1.amenities import api as amenities_api  # Note the leading dot
from .api.v1.reviews import api as reviews_api  # Note the leading dot
from .api.v1.places import api as places_api  # Note the leading dot

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    api.add_namespace(amenities_api, path='/api/v1/amenities')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(reviews_api, path='/api/v1/reviews')
    api.add_namespace(places_api, path='/api/v1/places')
    return app
