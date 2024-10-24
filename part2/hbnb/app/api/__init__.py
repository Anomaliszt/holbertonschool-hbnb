from flask_restx import Api
from .v1.amenities import api as amenities_ns  # Use relative import

api = Api(
    title='HBnB API',
    version='1.0',
    description='A simple API for the HBnB project',
)

api.add_namespace(amenities_ns, path='/api/v1/amenities')
