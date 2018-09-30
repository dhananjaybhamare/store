from flask_restful import reqparse, abort, Api, Resource
from . import api as api_blueprint
from app.service import shopping_service

api = Api(api_blueprint)


class ShoppingList(Resource):
    def post(self):
        """
        Restful endpoint to add a new shopping list.
        :return: shopping_list_id
        """
        parser = get_shopping_list_post_req_parser()
        args = parser.parse_args()
        title = args['title']
        store_name = args['store']
        shopping_list_id = shopping_service.add_shopping_list(title, store_name)
        if not shopping_list_id:
            abort(409, message='Shopping List already exist')
        return {"shopping_list_id": shopping_list_id}, 201

    def put(self):
        """
        Restful endpoint to update title/store_name of the shopping list
        :return: shopping_list_id
        """
        parser = get_shopping_list_put_req_parser()
        args = parser.parse_args()
        shopping_list_id = args['id']
        title = args['title']
        store_name = args['store']
        if not title and not store_name:
            abort(400, message='Either title or store name is required')
        shopping_list_id = shopping_service.update_shopping_list(shopping_list_id, title, store_name)
        if not shopping_list_id:
            abort(409, message='Shopping List does not exist')
        return {"shopping_list_id": shopping_list_id}, 201

    def delete(self):
        """
        Restful endpoint to delete the shopping list
        :return:
        """
        parser = get_shopping_list_delete_req_parser()
        args = parser.parse_args()
        shopping_list_id = args['id']
        shopping_list_id = shopping_service.delete_shopping_list(shopping_list_id)
        if not shopping_list_id:
            abort(409, message='Shopping List does not exist')
        return '', 204


class ShoppingListItem(Resource):
    def put(self):
        """
        Restful endpoint to add item in the shopping list
        :return: shopping list contents
        """
        parser = get_shopping_list_item_put_req_parser()
        args = parser.parse_args()
        shopping_list_id = args['shopping_list_id']
        item_id = args['item_id']
        quantity = args['quantity']

        item = shopping_service.get_item(item_id)
        if not item:
            abort(409, message='Item does not exist')

        shopping_list = shopping_service.get_shopping_list(shopping_list_id)
        if not shopping_list:
            abort(409, message='Shopping List does not exist')

        data = shopping_service.add_item_to_shopping_list(shopping_list, item, quantity)

        return data, 201


def get_shopping_list_post_req_parser():
    """
    Creates request parser for ShoppingList.post method
    :return: parser
    """
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=non_empty_string_argument, required=True, location='json')
    parser.add_argument('store', type=non_empty_string_argument, required=True, location='json')
    return parser


def get_shopping_list_put_req_parser():
    """
    Creates request parser for ShoppingList.put method
    :return: parser
    """
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True, location='json')
    parser.add_argument('title', type=str, required=False, location='json')
    parser.add_argument('store', type=str, required=False, location='json')
    return parser


def get_shopping_list_item_put_req_parser():
    """
    Creates request parser for ShoppingListItem.put method
    :return: parser
    """
    parser = reqparse.RequestParser()
    parser.add_argument('shopping_list_id', type=int, required=True, location='json')
    parser.add_argument('item_id', type=int, required=True, location='json')
    parser.add_argument('quantity', type=int, required=True, location='json')
    return parser


def non_empty_string_argument(value, name):
    """
    Validates of the request parameter string is not empty
    :param value:
    :param name:
    :return: value
    """
    if not value:
        raise ValueError('{} is not provided'.format(name))
    return value


def get_shopping_list_delete_req_parser():
    """
    Creates request parser for ShoppingList.put method
    :return: parser
    """
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True, location='json')
    return parser


api.add_resource(ShoppingList, '/shoppingList')
api.add_resource(ShoppingListItem, '/shoppingListItem')
