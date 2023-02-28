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

class SubstrateType(FormEnum):
    GRAVEL = 'Gravel'
    SAND = 'Sand'
    CORAL = 'Crushed Coral'
    PEAT = 'Peat'
    MINERAL = 'Mineral'
    CLAY = 'Clay'
    LATERITE = 'Laterite'
    VERMICULITE = 'Vermiculite'
    AQUA = 'Aqua Soil'
    ONYX = 'Onyx'
    AKADAMA = 'Akadama'
    MIXED = 'Mixed/Multi-Layer'
    OTHER = 'Other'

class FilterType(FormEnum):
    NONE = 'None'
    HOB = 'HOB (Hang-On-Back)'
    SPONGE = 'Sponge'
    INTERNAL = 'Internal'
    CANISTER = 'Canister'
    SURFACE = 'Surface Skimmer'
    SUMP = 'Sump'
    UGF = 'Under Gravel'
    WD = 'Wet/Dry'
    PROTEIN = 'Protein Skimmer'
    OTHER = 'Other'

#item model
class Item(db.Model):
    """Tank Item Model"""
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Enum(LivestockType), default=LivestockType.OTHER)
    photo_url = db.Column(URLType)
    tank_id = db.Column(
        db.Integer, db.ForeignKey('tank.id'), nullable=False)
    tank = db.relationship('Tank', back_populates='items')

# user model
class User(UserMixin, db.Model):
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
    substrate = db.Column(db.Enum(SubstrateType), default=SubstrateType.OTHER)
    filtration = db.Column(db.Enum(FilterType), default=FilterType.OTHER)
    items = db.relationship('Item', back_populates='tank')

    def __str__(self):
        return self.name
