from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade  # Import the facade to interact with the business layer

# Create the API namespace for amenities
api = Namespace('amenities', description='Amenity operations')

# Define the Amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Instantiate the facade to handle logic
facade = HBnBFacade()

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        # Get the input data from the request
        data = api.payload
        
        # Create a new amenity using the facade
        new_amenity = facade.create_amenity(data)
        
        return {'message': 'Amenity successfully created', 'amenity': new_amenity}, 201

    @api.response(200, 'List of amenities retrieved successfully')

    def get(self):
        """Retrieve a list of all amenities"""
        # Get all amenities from the facade
        amenities = facade.get_all_amenities()

        return {'amenities': amenities}, 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        # Retrieve amenity details from the facade
        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {'message': 'Amenity not found'}, 404

        return {'amenity': amenity}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        # Get the input data from the request
        data = api.payload

        # Call the facade to update the amenity
        updated_amenity = facade.update_amenity(amenity_id, data)

        if not updated_amenity:
            return {'message': 'Amenity not found'}, 404

        return {'message': 'Amenity updated successfully', 'amenity': updated_amenity}, 200
  