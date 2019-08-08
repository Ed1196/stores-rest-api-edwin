
#Allows us to get access to the enviromental 
#variables declared within the host system, Heroku.
import os

from flask import Flask, jsonify, request
from datetime import timedelta

#Resource: The resource that the Api is concernt with
#reqparse: Will allow us to parse http request for only ther data that is needed
from flask_restful import Resource, Api, reqparse

#Will allow us use JWT with our app
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserList, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST


app = Flask(__name__)
#Api: Allow us to add/remove/update resources, all have to be a class
api = Api(app)

#Key that will be use for decryption
app.secret_key = 'Edwin'

#Tells sqlAlchemy where to find the data.db file
                        #If the app can't find the enviromental variable, then use the second connection
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

#Its sort of a listener
# In order to know when an object changes, but not changed in the database
# extension flask_sqlalchemy was tracking it. However we dont need it because
# SQLAlchemy already has a tracker built into its library
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# If Flask-JWT raises an error, then the Flask app will not see the error, unless this is true
app.config['PROPAGATE_EXCEPTIONS'] = True

# Configuration for enabling blacklisting.
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
# enable blacklist if a blacklisted id is using a access or refresh token.
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']

#WILL ONLY BE USED LOCALLY
# With this flask decorator will run the method below it before the first request
# db.create_all() will create all the tables in the database
#@app.before_first_request
#def create_tables():
#    db.create_all()

jwt = JWTManager(app)  # No longer creates an /auth endpoint

#JWT CLAIMS
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'isAdmin': True}
    else:
        return {'isAdmin': False}

# Configuring jwt_extended callbacks and responses.
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

# Error sent when user sents an non_jwt string
@jwt.invalid_token_loader
def expired_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_jwt'
    }), 401

@jwt.unauthorized_loader
def unauthorized_token_callback(error):
    return jsonify({
        'description': 'No auth token was present.',
        'error': 'auth_jwt_required'
    }), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401

# decrypted_token: We can access any data of the token.
# decrypted_token is the user's id and it will check if it's in the BLACKLIST
# If in the black list, call @jwt.revoke_token_loader()
# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST  # Here we blacklist particular users.

# Prevent a previously auth token from accessing resources that
# require authentication.
@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401

@app.route("/", methods = ['GET'])
def homePage():
    return "This is Edwin's API, nothing to see here :)"


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
#add_resource: adds a resource to the API
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/student/Edwin
api.add_resource(ItemList, '/items')
#When this endpoint gets hit, the UserRegister post method gets called
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
#With JWT_Extended we have to declare the endpoint.
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh,'/refresh')
api.add_resource(UserList, '/users')

api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    #Circular import
    from db import db
    #Register sqlAlchemy extension to the app
    db.init_app(app)
    app.run(port=5000, debug=True)
