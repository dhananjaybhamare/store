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

    def test_shopping_list_creation(self):
        """
        Unittest: Add new shopping list: successful
        :return:
        """
        res = self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': 'Amazon'}))
        self.assertEqual(res.status_code, 201)
        self.assertIn('shopping_list_id', str(res.data))
        self.assertIn('1', str(res.data))

    def test_shopping_list_creation_error_1(self):
        """
        Unittest: Add new shopping list: Failed
        Attempt to add already existing shopping list
        :return:
        """
        res = self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': 'Amazon'}))
        self.assertEqual(res.status_code, 201)
        self.assertIn('shopping_list_id', str(res.data))

        res = self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': 'Amazon'}))
        self.assertEqual(res.status_code, 409)
        self.assertIn('Shopping List already exist', str(res.data))

    def test_shopping_list_creation_error_2(self):
        """
        Unittest: Add new shopping list: failed
        Validation error - store not provided
        :return:
        """
        res = self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': ''}))
        self.assertEqual(res.status_code, 400)
        self.assertIn('store is not provided', str(res.data))

    def test_shopping_list_creation_error_3(self):
        """
        Unittest: Add new shopping list: failed
        Validation error - title not provided
        :return:
        """
        res = self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': '', 'store': 'Amazon'}))
        self.assertEqual(res.status_code, 400)
        self.assertIn('title is not provided', str(res.data))

    def test_shopping_list_creation_error_4(self):
        """
        Unittest: Add new shopping list: failed
        Validation error - title not provided
        :return:
        """
        res = self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': '', 'store': ''}))
        self.assertEqual(res.status_code, 400)
        self.assertIn('title is not provided', str(res.data))

    def test_shopping_list_update_title(self):
        """
        Unittest: Update shopping list: successful
        Title updated successfully
        :return:
        """
        self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': 'Amazon'}))

        res = self.client().put(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({"id": 1, "title": "Grocery New", "store": ""}))
        self.assertEqual(res.status_code, 201)
        self.assertIn('shopping_list_id', str(res.data))
        self.assertIn('1', str(res.data))

    def test_shopping_list_update_store(self):
        """
        Unittest: Update shopping list: successful
        Store updated successfully
        :return:
        """
        self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': 'Amazon'}))

        res = self.client().put(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({"id": 1, "title": "", "store": "Amazon1"}))
        self.assertEqual(res.status_code, 201)
        self.assertIn('shopping_list_id', str(res.data))
        self.assertIn('1', str(res.data))

    def test_shopping_list_update_error_1(self):
        """
        Unittest: Update shopping list: failed
        Shopping list does not exist
        :return:
        """
        res = self.client().put(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({"id": 1, "title": "Grocery New", "store": ""}))
        self.assertEqual(res.status_code, 409)
        self.assertIn('Shopping List does not exist', str(res.data))

    def test_shopping_list_update_error_2(self):
        """
        Unittest: Update shopping list: failed
        Either title or store name is required
        :return:
        """
        self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': 'Amazon'}))

        res = self.client().put(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({"id": 1, "title": "", "store": ""}))
        self.assertEqual(res.status_code, 400)
        self.assertIn('Either title or store name is required', str(res.data))

    def test_shopping_list_update_error_3(self):
        """
        Unittest: Update shopping list: failed
        Shopping list id is not integer
        :return:
        """
        self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': 'Amazon'}))

        res = self.client().put(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({"id": "id", "title": "", "store": ""}))
        self.assertEqual(res.status_code, 400)
        self.assertIn('invalid literal for int', str(res.data))

    def test_shopping_list_delete(self):
        """
        Unittest: Delete shopping list: successful
        :return:
        """
        self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': 'Amazon'}))

        res = self.client().delete(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({"id": 1}))
        self.assertEqual(res.status_code, 204)

    def test_shopping_list_delete_error_1(self):
        """
        Unittest: Delete shopping list: failed
        Shopping List does not exist
        :return:
        """
        res = self.client().delete(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({"id": 1}))
        self.assertEqual(res.status_code, 409)
        self.assertIn('Shopping List does not exist', str(res.data))

    def test_shopping_list_delete_error_2(self):
        """
        Unittest: Delete shopping list: failed
        Shopping list id is not integer
        :return:
        """
        res = self.client().delete(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({"id": "id"}))
        self.assertEqual(res.status_code, 400)
        self.assertIn('invalid literal for int', str(res.data))

    def test_shopping_list_add_item(self):
        """
        Unittest: Add item in shopping list: successful
        :return:
        """
        self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': 'Amazon'}))

        res = self.client().put(
            '/api/v1/shoppingListItem',
            content_type='application/json',
            data=json.dumps({"shopping_list_id": 1, "item_id": 1, "quantity": 1}))

        self.assertEqual(res.status_code, 201)
        self.assertIn('"shopping_list_title": "Grocery", "store_name": "Amazon"', str(res.data))
        self.assertIn('"item_title": "Water Bottle"', str(res.data))

    def test_shopping_list_add_item_error_1(self):
        """
        Unittest: Add item in shopping list: failed
        Missing required parameter - shopping_list_id
        :return:
        """
        self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': 'Amazon'}))

        res = self.client().put(
            '/api/v1/shoppingListItem',
            content_type='application/json',
            data=json.dumps({"item_id": 1, "quantity": 1}))

        self.assertEqual(res.status_code, 400)
        self.assertIn('Missing required parameter', str(res.data))

    def test_shopping_list_add_item_error_2(self):
        """
        Unittest: Add item in shopping list: failed
        Missing required parameter - item_id
        :return:
        """
        self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': 'Amazon'}))

        res = self.client().put(
            '/api/v1/shoppingListItem',
            content_type='application/json',
            data=json.dumps({"shopping_list_id": 1, "quantity": 1}))

        self.assertEqual(res.status_code, 400)
        self.assertIn('Missing required parameter', str(res.data))

    def test_shopping_list_add_item_error_3(self):
        """
        Unittest: Add item in shopping list: failed
        Missing required parameter - quantity
        :return:
        """
        self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': 'Amazon'}))

        res = self.client().put(
            '/api/v1/shoppingListItem',
            content_type='application/json',
            data=json.dumps({"shopping_list_id": 1, "item_id": 1}))

        self.assertEqual(res.status_code, 400)
        self.assertIn('Missing required parameter', str(res.data))

    def test_shopping_list_add_item_error_4(self):
        """
        Unittest: Add item in shopping list: failed
        Shopping List does not exist
        :return:
        """
        res = self.client().put(
            '/api/v1/shoppingListItem',
            content_type='application/json',
            data=json.dumps({"shopping_list_id": 1, "item_id": 1, "quantity": 1}))

        self.assertEqual(res.status_code, 409)
        self.assertIn('Shopping List does not exist', str(res.data))

    def test_shopping_list_add_item_error_5(self):
        """
        Unittest: Add item in shopping list: failed
        Item does not exist
        :return:
        """
        self.client().post(
            '/api/v1/shoppingList',
            content_type='application/json',
            data=json.dumps({'title': 'Grocery', 'store': 'Amazon'}))

        res = self.client().put(
            '/api/v1/shoppingListItem',
            content_type='application/json',
            data=json.dumps({"shopping_list_id": 1, "item_id": 1000, "quantity": 1}))

        self.assertEqual(res.status_code, 409)
        self.assertIn('Item does not exist', str(res.data))
