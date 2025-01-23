from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, IntegerField, DateField
from wtforms import validators


class AddUser(FlaskForm):
    name = StringField('name', validators=[validators.length(min=3, max=100), validators.DataRequired()])
    gender = RadioField('gender', choices=['Male', 'Female'])
    salary = IntegerField(validators=[validators.NumberRange(min=0), validators.DataRequired()])
    date_of_birth = DateField(format='%Y-%m-%d', validators=[validators.DataRequired()])
