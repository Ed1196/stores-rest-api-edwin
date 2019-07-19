import sqlite3
from db import db;

# THIS IS A CLASS MODEL THAT WILL BE USE TO CREATE ALL THE USERS.
# WILL REDUCE THE CODE NEEDED
# db.Model: Extends db, tells sqlAlchemy entity that ItemModel
# will be an object that will be stored in a database.
class UserModel(db.Model):
    __tablename__ = 'users'
    # Specifies the tables, columns and rows in the database
    # This will make local variables from UserModel object to the values that
    # will be stored in the database

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
    #Used _id instead as id, as it is a python keyword
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def findByUserName(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def findById(cls, _id):
        return cls.query.filter_by(id = _id).first()
