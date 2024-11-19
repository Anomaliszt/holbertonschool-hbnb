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
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        review_data = api.payload
        user_id = get_jwt_identity()

        review_data['user_id'] = user_id
        new_review = facade.create_review(review_data)
        if new_review is None:
            return {'message': 'Invalid input data'}, 400
        return {
                "id": new_review.id,
                "text": new_review.text,
                "rating": new_review.rating,
                "user_id": new_review.user_id,
                "place_id": new_review.place_id
                }, 201

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
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        user_id = get_jwt_identity()
        data = api.payload
        try:
            review = facade.get_review(review_id)
            if review.user_id != user_id:
                return {'message': 'Unauthorized to update this review'}, 403
            updated_review = facade.update_review(review_id, data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 404

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized to delete this review')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        user_id = get_jwt_identity()
        try:
            review = facade.get_review(review_id)
            if not review:
                return {'message': 'Review not found'}, 404
            if review.user_id != user_id:
                return {'message': 'Unauthorized to delete this review'}, 403
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except ValueError:
            return {'message': 'Review not found'}, 404

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
        