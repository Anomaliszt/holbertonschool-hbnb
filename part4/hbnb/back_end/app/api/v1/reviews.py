from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

facade = HBnBFacade()

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data or validation error')
    @api.response(404, 'Place not found')
    @jwt_required()
    def post(self):
        """Register a new review"""
        review_data = api.payload.copy()
        user_identity = get_jwt_identity()
        user_id = user_identity['id'] if isinstance(user_identity, dict) else user_identity

        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'message': 'Place not found'}, 404
        if str(place.owner_id) == str(user_id):
            return {'message': 'You cannot review your own place'}, 400

        existing_review = facade.get_review_by_user_and_place(user_id, review_data['place_id'])
        if existing_review:
            return {'message': 'You have already reviewed this place'}, 400

        review_data['user_id'] = str(user_id)
        
        try:
            new_review = facade.create_review(review_data)
            return {
                "id": new_review.id,
                "text": new_review.text,
                "rating": new_review.rating,
                "user_id": new_review.user_id,
                "place_id": new_review.place_id
            }, 201
        except (ValueError, TypeError) as e:
            return {'message': f'Invalid input data: {str(e)}'}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{'id': r.id, 'text': r.text, 'rating': r.rating} for r in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if review:
            return {
                    "id": review.id,
                    "text": review.text,
                    "rating": review.rating,
                    "user_id": review.user_id,
                    "place_id": review.place_id
                    }, 200
        return {'message': 'Review not found'}, 404

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        user_identity = get_jwt_identity()
        user_id = user_identity['id'] if isinstance(user_identity, dict) else user_identity
        data = api.payload

        if not data or 'text' not in data or 'rating' not in data:
            return {'message': 'Missing required fields'}, 400

        if not isinstance(data['rating'], int) or not (1 <= data['rating'] <= 5):
            return {'message': 'Rating must be an integer between 1 and 5'}, 400

        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
            
        if review.user_id != user_id:
            return {'message': 'Unauthorized action'}, 403

        try:
            updated_review = facade.update_review(review_id, data)
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id
            }, 200
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        user_identity = get_jwt_identity()
        user_id = user_identity['id'] if isinstance(user_identity, dict) else user_identity
        
        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
            
        if review.user_id != user_id:
            return {'message': 'Unauthorized action'}, 403
            
        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            return {'message': 'Error deleting review'}, 500

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {"message": "Place not found"}, 404
        return [{'id': review.id, 'text': review.text, 'rating': review.rating} for review in reviews], 200
