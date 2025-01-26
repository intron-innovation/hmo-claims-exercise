from . import database
from datetime import datetime


class BaseModel(database.Model):
    __abstract__ = True

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    created_at = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    is_active = database.Column(database.Boolean, default=True)
    is_deleted = database.Column(database.Boolean, default=False)


# Register models here to enable migration
from .users.models import *
from .claims.models import *
