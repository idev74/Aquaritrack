from extensions import db
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

#user model
class User(db.Model):
    """User Model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return f'<User: {self.username}>'

#tank model
class Tank(db.Model):
    """Tank Model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    gallons = db.Column(db.Integer, nullable=False)
    substrate = db.Column(db.String(80), nullable=False)
    # created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # created_by = db.relationship('User')


#item model
class Item(db.Model):
    """Tank Item Model"""
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.Float(precision=2), nullable=False)
    # created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # created_by = db.relationship('User')

 
