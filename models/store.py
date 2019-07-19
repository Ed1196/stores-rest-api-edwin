from db import db

class StoreModel(db.Model):

    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    # Tells sqlAlchemy that there is a relationship with ItemModel
    # It is a list of ItemModel's since there is a many to one relationship
    # between a StoreModel and an ItemModel
    # As soon as we create a store model, we will create an item that matches that store_id
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name':self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
