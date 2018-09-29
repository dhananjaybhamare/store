from flask_restful import reqparse, abort, Api, output_json
from . import api as api_blueprint
from app.service import shopping_service

api = Api(api_blueprint)


@api_blueprint.route('/allShoppingList', methods=['GET'])
def get_all_shopping_list():
    """
    Restful endpoint to get all shopping lists with items
    :return: data
    """
    data = shopping_service.get_all_shopping_list()
    return output_json(data, 200)


@api_blueprint.route('/shoppingListByTitle/<title>', methods=['GET'])
def get_shopping_list_by_title(title):
    """
    Restful endpoint to get all shopping lists based on title
    :param title:
    :return: data
    """
    data = shopping_service.get_shopping_list_by_title(title)
    return output_json(data, 200)


@api_blueprint.route('/searchShoppingListsByTitle/<title>', methods=['GET'])
def search_shopping_list_by_title_keyword(title):
    """
    Restful endpoint to get all shopping lists which contains given keyword in title
    :param title:
    :return: data
    """
    data = shopping_service.search_shopping_list_by_title_keyword(title)
    return output_json(data, 200)


@api_blueprint.route('/shoppingListByItemId/<int:item_id>', methods=['GET'])
def get_shopping_list_by_item_id(item_id):
    """
    Restful endpoint to get all shopping lists containing given item
    :param item_id:
    :return: data
    """
    data = shopping_service.get_shopping_list_by_item_id(item_id)
    return output_json(data, 200)


@api_blueprint.route('/searchShoppingListByItemName/<title>', methods=['GET'])
def search_shopping_list_by_item_name_keyword(title):
    """
    Restful endpoint to get all shopping lists having item which contains given keyword in tile
    :param title:
    :return: data
    """
    data = shopping_service.search_shopping_list_by_item_name_keyword(title)
    return output_json(data, 200)