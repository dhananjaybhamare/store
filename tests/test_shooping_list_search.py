import unittest
import json
from app import create_app, db
from app.models import Item, UnitMeasurement


class ShoppingListAPITestCase(unittest.TestCase):
    def setUp(self):
        """
        Unittest setup method to initialize app in testing mode
        and create test data.
        :return:
        """
        self.app = create_app("testing")
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()
            UnitMeasurement.insert_unit_measurement()
            Item.insert_items()
            db.session.commit()

    def tearDown(self):
        """
        Unittest tear down method to remove data
        :return:
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_shopping_list(self):
        """
        Helper method to add three shopping lists - Grocery, Grocery New and Custom
        :return:
        """
        self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': 'Amazon'}))

        self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery New', 'store': 'Amazon'}))

        self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Custom', 'store': 'Amazon'}))

    def add_item_in_shopping_list(self):
        """
        Helper method to add item in already created shopping lists - Grocery, Grocery New and Custom
        Item - Water Bottle - is added in Grocery and Grocery New
        Item - Rice 1 KG Bag - is added in Custom
        Item - Rice 2 KG Bag - is added in Grocery
        :return:
        """
        self.client().put(
            '/api/v1/shoppingListItem',
            content_type='application/json',
            data=json.dumps({"shopping_list_id": 1, "item_id": 1, "quantity": 1}))

        self.client().put(
            '/api/v1/shoppingListItem',
            content_type='application/json',
            data=json.dumps({"shopping_list_id": 1, "item_id": 4, "quantity": 1}))

        self.client().put(
            '/api/v1/shoppingListItem',
            content_type='application/json',
            data=json.dumps({"shopping_list_id": 2, "item_id": 1, "quantity": 1}))

        self.client().put(
            '/api/v1/shoppingListItem',
            content_type='application/json',
            data=json.dumps({"shopping_list_id": 3, "item_id": 2, "quantity": 1}))

    def test_get_all_shopping_list(self):
        """
        Unittest: Get all shopping lists
        Shopping list not added
        :return:
        """
        res = self.client().get('/api/v1/allShoppingList')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"item_title": "Water Bottle"', str(res.data))

    def test_get_all_shopping_list_1(self):
        """
        Unittest: Get all shopping lists
        Shopping lists without items
        :return:
        """
        self.create_shopping_list()

        res = self.client().get('/api/v1/allShoppingList')
        self.assertEqual(res.status_code, 200)
        self.assertIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"item_title": "Water Bottle"', str(res.data))

    def test_get_all_shopping_list_2(self):
        """
        Unittest: Get all shopping lists
        Shopping lists with items
        :return:
        """
        self.create_shopping_list()
        self.add_item_in_shopping_list()

        res = self.client().get('/api/v1/allShoppingList')
        self.assertEqual(res.status_code, 200)
        self.assertIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertIn('"item_title": "Water Bottle"', str(res.data))

    def test_get_shopping_list_with_title(self):
        """
        Unittest: Get shopping list with title
        Shopping list not added
        :return:
        """
        res = self.client().get('/api/v1/shoppingListByTitle/Grocery')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"item_title": "Water Bottle"', str(res.data))

    def test_get_shopping_list_with_title_1(self):
        """
        Unittest: Get shopping list with title
        Shopping lists added
        :return:
        """
        self.create_shopping_list()

        res = self.client().get('/api/v1/shoppingListByTitle/Grocery')
        self.assertEqual(res.status_code, 200)
        self.assertIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Grocery New", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"item_title": "Water Bottle"', str(res.data))

    def test_get_shopping_list_with_title_2(self):
        """
        Unittest: Get shopping list with title
        Shopping lists added with items
        :return:
        """
        self.create_shopping_list()
        self.add_item_in_shopping_list()

        res = self.client().get('/api/v1/shoppingListByTitle/Grocery')
        self.assertEqual(res.status_code, 200)
        self.assertIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Grocery New", "store_name": "Amazon"', str(res.data))
        self.assertIn('"item_title": "Water Bottle"', str(res.data))

    def test_search_shopping_list_by_title_keyword(self):
        """
        Unittest: Search shopping list with title containing a keyword
        Shopping list not added
        :return:
        """
        res = self.client().get('/api/v1/searchShoppingListsByTitle/Grocery')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Grocery New", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Custom", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"item_title": "Water Bottle"', str(res.data))

    def test_search_shopping_list_by_title_keyword_1(self):
        """
        Unittest: Search shopping list with title containing a keyword
        Shopping lists added
        :return:
        """
        self.create_shopping_list()

        res = self.client().get('/api/v1/searchShoppingListsByTitle/Grocery')
        self.assertEqual(res.status_code, 200)
        self.assertIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertIn('"shopping_list_title": "Grocery New", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Custom", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"item_title": "Water Bottle"', str(res.data))

    def test_search_shopping_list_by_title_keyword_2(self):
        """
        Unittest: Search shopping list with title containing a keyword
        Shopping lists added with items
        :return:
        """
        self.create_shopping_list()
        self.add_item_in_shopping_list()

        res = self.client().get('/api/v1/searchShoppingListsByTitle/Grocery')
        self.assertEqual(res.status_code, 200)
        self.assertIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertIn('"shopping_list_title": "Grocery New", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Custom", "store_name": "Amazon"', str(res.data))
        self.assertIn('"item_title": "Water Bottle"', str(res.data))

    def test_search_shopping_list_by_title_keyword_3_error(self):
        """
        Unittest: Search shopping list with title containing a keyword
        Title is not sent in URL
        :return:
        """
        self.create_shopping_list()
        self.add_item_in_shopping_list()

        res = self.client().get('/api/v1/searchShoppingListsByTitle')
        self.assertEqual(res.status_code, 404)
        self.assertNotIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Grocery New", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Custom", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"item_title": "Water Bottle"', str(res.data))

    def test_get_shopping_list_by_item_id(self):
        """
        Unittest: Get all shopping list having given item added
        Shopping list not added
        :return:
        """
        res = self.client().get('/api/v1/shoppingListByItemId/1')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"item_title": "Water Bottle"', str(res.data))

    def test_get_shopping_list_by_item_id_1(self):
        """
        Unittest: Get all shopping list having given item added
        Shopping lists added
        :return:
        """
        self.create_shopping_list()

        res = self.client().get('/api/v1/shoppingListByItemId/1')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Grocery New", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Custom", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"item_title": "Water Bottle"', str(res.data))

    def test_get_shopping_list_by_item_id_2(self):
        """
        Unittest: Get all shopping list having given item added
        Shopping lists added with items
        :return:
        """
        self.create_shopping_list()
        self.add_item_in_shopping_list()

        res = self.client().get('/api/v1/shoppingListByItemId/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertIn('"shopping_list_title": "Grocery New", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Custom", "store_name": "Amazon"', str(res.data))
        self.assertIn('"item_title": "Water Bottle"', str(res.data))

    def test_get_shopping_list_by_item_id_3_error(self):
        """
        Unittest: Get all shopping list having given item added
        Id not sent in URL
        :return:
        """
        self.create_shopping_list()
        self.add_item_in_shopping_list()

        res = self.client().get('/api/v1/shoppingListByItemId')
        self.assertEqual(res.status_code, 404)
        self.assertNotIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Grocery New", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Custom", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"item_title": "Water Bottle"', str(res.data))

    def test_get_shopping_list_by_item_id_4_error(self):
        """
        Unittest: Get all shopping list having given item added
        Non integer id is sent in URL
        :return:
        """
        self.create_shopping_list()
        self.add_item_in_shopping_list()

        res = self.client().get('/api/v1/shoppingListByItemId/not_integer')
        self.assertEqual(res.status_code, 404)
        self.assertNotIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Grocery New", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Custom", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"item_title": "Water Bottle"', str(res.data))

    def test_search_shopping_list_by_item_name_keyword(self):
        """
        Unittest: Search all shopping list having given item containing keyword in title
        Shopping list not added
        :return:
        """
        res = self.client().get('/api/v1/searchShoppingListByItemName/Water')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"item_title": "Water Bottle"', str(res.data))

    def test_search_shopping_list_by_item_name_keyword_1(self):
        """
        Unittest: Search all shopping list having given item containing keyword in title
        Shopping lists added
        :return:
        """
        self.create_shopping_list()

        res = self.client().get('/api/v1/searchShoppingListByItemName/Water')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Grocery New", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Custom", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"item_title": "Water Bottle"', str(res.data))

    def test_search_shopping_list_by_item_name_keyword_2(self):
        """
        Unittest: Search all shopping list having given item containing keyword in title
        Shopping lists added with items
        :return:
        """
        self.create_shopping_list()
        self.add_item_in_shopping_list()

        res = self.client().get('/api/v1/searchShoppingListByItemName/Water')
        self.assertEqual(res.status_code, 200)
        self.assertIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertIn('"shopping_list_title": "Grocery New", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Custom", "store_name": "Amazon"', str(res.data))
        self.assertIn('"item_title": "Water Bottle"', str(res.data))

    def test_search_shopping_list_by_item_name_keyword_3_error(self):
        """
        Unittest: Search all shopping list having given item containing keyword in title
        Title not sent in URL
        :return:
        """
        self.create_shopping_list()
        self.add_item_in_shopping_list()

        res = self.client().get('/api/v1/searchShoppingListByItemName')
        self.assertEqual(res.status_code, 404)
        self.assertNotIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Grocery New", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"shopping_list_title": "Custom", "store_name": "Amazon"', str(res.data))
        self.assertNotIn('"item_title": "Water Bottle"', str(res.data))
