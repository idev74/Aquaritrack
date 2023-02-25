from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from aquaritrack.models import LivestockType, User, Tank, Item

class ItemForm(FlaskForm):
    """Form to create an item"""
    species = StringField('Species',
        validators=[DataRequired(), Length(min=2, max=80)])
    quantity = IntegerField('Quantity',
        validators=[DataRequired()])
    category = SelectField('Category', choices=LivestockType.choices())
    photo_url = StringField('Photo URL',
        validators=[DataRequired()])
    submit = SubmitField('Submit')


class TankForm(FlaskForm):
    """Form to create a tank."""
    name = StringField('Author Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    biography = TextAreaField('Author Biography')
    submit = SubmitField('Submit')

# class UserForm(FlaskForm):
#     """Form to create a user."""

