from security import authenticate, identity
from flask import Flask, jsonify, request
from datetime import timedelta

#Resource: The resource that the Api is concernt with
#reqparse: Will allow us to parse http request for only ther data that is needed
from flask_restful import Resource, Api, reqparse

#Will allow us use JWT with our app
from flask_jwt import JWT, jwt_required
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
#Api: Allow us to add/remove/update resources, all have to be a class
api = Api(app)

# With this flask decorator will run the method below it before the first request
# db.create_all() will create all the tables in the database
@app.before_first_request
def create_tables():
    db.create_all()

#Key that will be use for decryption
app.secret_key = 'Edwin'

#We must change the JWT authentication URL first, before creating the JWT instance
app.config['JWT_AUTH_URL_RULE'] = '/login'

#config JWT to expire within hald an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds = 1800)

#config JWT auth key name to be 'email' instead of default 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

#Tells sqlAlchemy where to find the data.db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

#Its sort of a listener
# In order to know when an object changes, but not changed in the database
# extension flask_sqlalchemy was tracking it. However we dont need it because
# SQLAlchemy already has a tracker built into its library
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#JWT: Will create a new endpoint
    #we send JWT a user name and a password
        #then it will call the authenticate method
        #if authentication is good, a JWT token will be sent back and stored in jwt
    #JWT will only use the identity_function when it sends a JWT token
jwt = JWT(app, authenticate, identity)  # /auth, /login after 'JWT_AUTH_URL_RULE'

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'authorization' : access_token.decode('utf-8'),
        'user_id': identity.id
    })




api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
#add_resource: adds a resource to the API
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/student/Edwin
api.add_resource(ItemList, '/items')
#When this endpoint gets hit, the UserRegister post method gets called
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    #Circular import
    from db import db
    #Register sqlAlchemy extension to the app
    db.init_app(app)
    app.run(port=5000, debug=True)
