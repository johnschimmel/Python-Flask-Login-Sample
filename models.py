import datetime
from app import db

class User(db.Document):
	email = db.EmailField(unique=True)
	password = db.StringField(default=True)
	active = db.BooleanField(default=True)
	isAdmin = db.BooleanField(default=False)
	timestamp = db.DateTimeField(default=datetime.datetime.now())
    
class Note(db.Document):
    title = db.StringField(required=True,max_length=120)
    content = db.StringField()
    last_updated = db.DateTimeField(default=datetime.datetime.now())
    user = db.ReferenceField(User)
    