from flask_restx import Namespace, Resource, fields
from flask_cors import cross_origin
from flask import make_response
from flask_jwt_extended import create_access_token
from app.services.facade import HBnBFacade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

facade = HBnBFacade()

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @cross_origin()
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload

        try:
            user = facade.get_user_by_email(credentials['email'])

            if not user or not user.verify_password(credentials['password']):
                return {'error': 'Invalid credentials'}, 401

            access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
            return {'access_token': access_token}, 200

        except Exception as e:
            return {'error': 'Authentication failed'}, 500