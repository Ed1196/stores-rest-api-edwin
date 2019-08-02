import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity,
    jwt_refresh_token_required)

#Variable that will allow us to parse the data
_user_parser = reqparse.RequestParser()
#Here is where we specify the fields that we want from the payload
_user_parser.add_argument('username',
        type=str,
        required=True,
        help='This field cannot be left blank!')
_user_parser.add_argument('password',
        type=str,
        required=True,
        help='This field cannot be left blank!')

class UserRegister(Resource):

    def post(self):
        #We store the data that we parsed into a variable
        data =  _user_parser.parse_args()

        #Check if user already exists: Use the findByUserName method from User
        if(UserModel.findByUserName(data['username']) ):
            return {'message':'User already exists'}, 409


        user = UserModel(**data)
        user.save_to_db()

        return {'message':'User was created succesfully!'}, 201

class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.findById(user_id) 
        if user is not None:
            return {'user': user.json()}

    @classmethod
    def delete(cls, user_id):
        user = UserModel.findById(user_id)
        if user is not None:
            user.delete_from_db()
            return {'message': 'User deleted succesfully.'}
        return {'message': 'User does not exist.'}

class UserLogin(Resource):
   

    @classmethod
    def post(cls):
        # get data from parser
        data =  _user_parser.parse_args()
        # find user in database
        user = UserModel.findByUserName(data['username'])
        # check password
        # create access token
        # create refresh token
        if user and safe_str_cmp(user.password, data['password']):
            #JWT_Ex creates the JWT here that the user will use to make calls to the api
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid Credentials'}, 401
        
class TokenRefresh(Resource):
    @jwt_refresh_token_required # Deny access if refresh_token is not in the request.
    def get(self):
        current_user = get_jwt_identity()
        # If fresh==True; password and username was given to us.
        # If fresh==False; password and username were given days ago.
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200