from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.api.v1.users import user_model
from app.api.v1.amenities import amenity_model
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})

facade = HBnBFacade()

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        place_data = api.payload
        user = facade.get_user(place_data.get('owner_id'))
        if user is None:
            return {'error': 'Invalid owner_id.'}, 400

        if current_user['id'] != user.id:
            return {'error': 'Unauthorized action.'}, 403

        if place_data.get('amenities'):
            for amenity in place_data.get('amenities'):
                if facade.get_amenity(amenity['id']) is None:
                    return {'error': 'Invalid amenity ID.'}, 400

        try:
            place = facade.create_place(place_data)
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': str(place.price),
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner_id,
                }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude
        } for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': place.owner_id,
            'amenities': place.amenities,
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required
    def put(self, place_id):
        """
        Update a place's information
        Only the owner of the place can modify its details.
        Requires valid JWT token in Authorization header.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
            
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403
            
        try:
            place_data = api.payload
            if not is_admin:
                place_data.pop('owner_id', None)
            
            place_update = facade.update_place(place_id, place_data)
            return {
                'id': place_update.id,
                'title': place_update.title,
                'description': place_update.description,
                'latitude': place_update.latitude,
                'longitude': place_update.longitude,
                'owner_id': place_update.owner_id,
                'amenities': place_update.amenities
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})