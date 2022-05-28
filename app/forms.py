from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField, IntegerField, DateField, DateTimeField
from wtforms import validators
from app.models import User

all_users = User.query.with_entities(User.name).all()


class AddUser(FlaskForm):
    name = StringField('name', validators=[validators.length(min=3, max=100), validators.DataRequired()])
    gender = RadioField('gender', choices = ['male', 'female'])
    salary = IntegerField(validators=[validators.NumberRange(min=0), validators.DataRequired()])
    date_of_birth = DateField(format='%Y-%m-%d', validators=[validators.DataRequired()])