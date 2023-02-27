from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, ValidationError
from aquaritrack.models import LivestockType, SubstrateType, FilterType, User, Tank, Item

class ItemForm(FlaskForm):
    """Form to create an item"""
    species = StringField('Species',
        validators=[DataRequired(), Length(min=2, max=80)])
    quantity = IntegerField('Quantity',
        validators=[DataRequired()])
    category = SelectField('Category', choices=LivestockType.choices())
    photo_url = StringField('Photo URL',
        validators=[DataRequired()])
    tank = QuerySelectField('Tanks', validators=[DataRequired()], query_factory=lambda: Tank.query)
    submit = SubmitField('Submit')


class TankForm(FlaskForm):
    """Form to create a tank."""
    name = StringField('Tank Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    gallons = IntegerField('# of Gallons', 
        validators=[DataRequired()])
    substrate = SelectField('Substrate', choices=SubstrateType.choices())
    filtration = SelectField('Filter', choices=FilterType.choices())
    submit = SubmitField('Submit')
