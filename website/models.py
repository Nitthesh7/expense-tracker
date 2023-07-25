from . import db
from flask_login import UserMixin
from datetime import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    expenses = db.relationship('Entry') # this is a one-many relationship (category-entry)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    category = db.Column(db.String(30), db.ForeignKey('category.name'))
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    expenses = db.relationship('Entry') # this is a one-many relationship (user-entry)
    categories = db.relationship('Category') # this is a one-many relationship (user-category)

