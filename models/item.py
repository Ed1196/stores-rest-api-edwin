from db import db

# db.Model: Extends db, tells sqlAlchemy entity that ItemModel
# will be an object that will be stored in a database.
class ItemModel(db.Model):
    
    __tablename__ = "items"

    #Items local colums
    id = db.Column(db.Integer,  primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # Items foreign key: This is the relationship between item and store
    # Foreign keys will prevent linked items from being deleted.
    # Every item will be linked to a store,
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # Equivalent of a join in sequel
    store = db.relationship('StoreModel')


    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    #Return a JSON representation of a model
    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        # query: Comes from db.Model; query builder
        # SELECT * FROM items WHERE name = name LIMIT 1
        return ItemModel.query.filter_by(name=name).first()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    #WIll do both update and insert
    def save_to_db(self):
        #Update Object to row
        #self has id, name, price
        #session: collection of objects that will be written to the database
        db.session.add(self)
        db.session.commit()
