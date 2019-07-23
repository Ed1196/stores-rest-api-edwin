from app import app
from db import db

db.init_app(app)

# With this flask decorator will run the method below it before the first request
# db.create_all() will create all the tables in the database
@app.before_first_request
def create_tables():
    db.create_all()
