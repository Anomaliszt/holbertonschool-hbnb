from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

facade = HBnBFacade()

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized - Admin access required')
    def post(self):
        """Create a new amenity (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'message': 'Admin access required'}, 403

        data = api.payload
        try:
            amenity = facade.create_amenity(data)
            return {
                'id': amenity.id,
                'name': amenity.name
            }, 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception:
            return {'message': 'Failed to create amenity'}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 'name': amenity.name} for amenity in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            return {'id': amenity.id, 'name': amenity.name}, 200
        except ValueError as e:
            return {'message': str(e)}, 404

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized - Admin access required')
    def put(self, amenity_id):
        """Update an amenity's information (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'message': 'Admin access required'}, 403

        try:
            updated_amenity = facade.update_amenity(amenity_id, api.payload)
            return {'message': 'Amenity updated successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 400 if 'Invalid' in str(e) else 404