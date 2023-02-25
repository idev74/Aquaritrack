from sqlalchemy_utils import URLType
from flask_login import UserMixin
from sqlalchemy.orm import backref
from aquaritrack.extensions import db
import enum

class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)

class LivestockType(FormEnum):
    PLANT = 'Plant'
    FISH = 'Fish'
    INVERTEBRATE = 'Invertebrate'
    AMPHIBIAN = 'Amphibian'
    OTHER = 'other'

#item model
class Item(db.Model):
    """Tank Item Model"""
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Enum(LivestockType), default=LivestockType.OTHER)
    photo_url = db.Column(URLType)
    # TODO: add tank relationship, created_by, & created_by_id

# user model
class User(db.Model):
    # use mixin when doing tank
    """User Model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return f'<User: {self.username}>'

# tank model
class Tank(db.Model):
    """Tank Model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    gallons = db.Column(db.Integer, nullable=False)
    substrate = db.Column(db.String(80), nullable=False)
        # TODO: add item relationship, created_by, & created_by_id



 
