from .extensions import db 

class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)