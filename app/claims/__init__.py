from flask import Blueprint

claims = Blueprint('claims', __name__, template_folder="templates")

from . import views
