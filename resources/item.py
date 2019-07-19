from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from models.store import StoreModel

#Item becomes a class with the Resource class properties due to inheritance
#This is a resource that is only allowed to be accessed via GET
#404: Not found
#200: Most popular HTTP status code for OK
class Item(Resource):

    #This will parse the data before the function ever uses it and also allows us to put some
    #safeguards and restrictions on how the data is being passed down.
    #This request will stop, if the json payload does not have the correct 'price' format
    #The json payload could have multiple fields, but it will only take 'price'
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank!')
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='Every item needs a store id.')

    #Forces authentication before we reach the get method, will call the 'identity()' method from security
    @jwt_required()
    def get(self, name):
        #THIS IS ALL THE SET UP NEEDED TO RETRIEVE AN ITEM FROM THE DB
        try:
            #Returns an item object and not a dictionary, we must make it a json
            item = ItemModel.find_by_name(name)
        except:
            return {'message':'An error occurred finding an item!'}

        if item is not None:
            return item.json()

        return {'message':'Item was not found!'}



    #201: HTTP status code that stands for an item being created.
    #400: HTTP status code that stands for Bad Request
    #We want to make sure we have unique items
    def post(self, name):
        #Check if the item is already in the database
        if ItemModel.find_by_name(name) is not None:
            return {'message':"Item '{}' already exists!".format(name)}, 400

        #Request will take the data from the body of an HTTP request and convert it into a dictionary
        # data will have the fields needed to create an item; data['price'] for example
        #depricated by reqparse: data = request.get_json()
        data = Item.parser.parse_args()

        #Create a JSON of the item
        #Depricated: item = {'name':name, 'price':data['price']}
        item = ItemModel(name, data['price'], data['store_id'])

        if StoreModel.find_by_id(data['store_id']):
            item.save_to_db()
            return item.json(), 201
        else:
            return {'message':'Store does not exists!'}




    #Will delete an item from the list by filtering out the name of the item to be removed from the list
    def delete(self, name):
        #Finds item by its name
        item = ItemModel.find_by_name(name)

        if item is not None:
            # item calls its delete function to delete itself
            item.delete_from_db()
            return {'message': 'Item succesfully deleted!'}

        return {'message':'Item was not found!'}


    #Will update an item if the specified name already exists, or update it if it doesn't
    def put(self,name):

        #Request will take the data from the body of an HTTP request and convert it into a dictionary
        # data will have the fields needed to create an item; data['price'] for example
        #depricated by reqparse: data = request.get_json()
        data = Item.parser.parse_args()

        try:
            #if item exists, find it and store it into variable item
            item = ItemModel.find_by_name(name)
        except:
            return {'message': 'An error ocurred finding the item!'} , 500

        if item is None:
            #if item is None, create a new instance of ItemModel that will have an insert function
            item = ItemModel(name, **data)

        else:
            #If item does exists, we can manipulate its values
            item.price = data['price']
            item.store_id = data['store_id']

        #Because item is unique, sqlAlchemy will reconginize it and update it
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
       #return {'items': [list(map(lambda x: x.json(), ItemModel.query.all() ))]}
