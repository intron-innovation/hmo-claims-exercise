from datetime import datetime, date
from app import database
from app.models import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    name = database.Column(database.String(100), nullable=False, unique=True)
    salary = database.Column(database.Integer, nullable=False)
    gender = database.Column(database.String(10), nullable=True)
    date_of_birth = database.Column(database.Date, nullable=True)
    time_created = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    claim = database.relationship('Claim')

    def __repr__(self):
        return '<User: {}>'.format(self.name)

    @property
    def age(self):
        return int(date.today().year - self.date_of_birth.year)
