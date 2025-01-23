from flask import Blueprint

claims = Blueprint('claims', __name__)

from . import views
