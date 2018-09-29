from flask import Blueprint

api = Blueprint('api', __name__)

from . import shopping_list, shopping_list_search
