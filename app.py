
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
from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList


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

# With this flask decorator will run the method below it before the first request
# db.create_all() will create all the tables in the database
@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)  # No longer creates an /auth endpoint

#JWT CLAIMS
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'isAdmin': True}
    else:
        return {'isAdmin': False}


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

if __name__ == '__main__':
    #Circular import
    from db import db
    #Register sqlAlchemy extension to the app
    db.init_app(app)
    app.run(port=5000, debug=True)
