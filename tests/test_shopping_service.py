import unittest
from app import create_app, db
from app.models import Item, UnitMeasurement, ShoppingList
from app.service import shopping_service


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        """
        Unittest setup method to initialize app in testing mode
        and create test data.
        :return:
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        UnitMeasurement.insert_unit_measurement()
        Item.insert_items()
        db.session.commit()

    def tearDown(self):
        """
        Unittest tear down method to remove data
        :return:
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def add_shooping_list(self, title, store_name):
        """
        Helper method to add shopping list
        :param title:
        :param store_name:
        :return:
        """
        shopping_service.add_shopping_list('test_title', 'test_store')

    def test_add_shopping_list(self):
        """
        Unittest : Add shopping list - successful
        :return:
        """
        res = shopping_service.add_shopping_list('test_title', 'test_store')
        self.assertTrue(ShoppingList.query.filter_by(title='test_title').first() is not None)
        self.assertTrue(res == 1)

    def test_add_shopping_list_fail(self):
        """
        Unittest : Add same shopping list twice - second time it fails
        :return:
        """
        self.add_shooping_list('test_title', 'test_store')
        res = shopping_service.add_shopping_list('test_title', 'test_store')
        self.assertTrue(ShoppingList.query.filter_by(title='test_title').first() is not None)
        self.assertFalse(res == 1)

    def test_get_item(self):
        """
        Unittest : Get item - success
        :return:
        """
        res = shopping_service.get_item(1)
        self.assertTrue(res.id == 1)

    def test_get_item_fail(self):
        """
        Unittest : Get item - fail
        :return:
        """
        res = shopping_service.get_item(100)
        self.assertTrue(res is None)

    def test_get_shopping_list(self):
        """
        Unittest : Get shopping list - success
        :return:
        """
        self.add_shooping_list('test_title', 'test_store')
        res = shopping_service.get_shopping_list(1)
        self.assertTrue(res.id == 1)

    def test_get_shopping_list_fail(self):
        """
        Unittest : Get shopping list - fail
        :return:
        """
        res = shopping_service.get_shopping_list(1)
        self.assertTrue(res is None)

    def test_add_item_to_shopping_list(self):
        """
        Unittest : Add item to shopping list - success
        :return:
        """
        self.add_shooping_list('test_title', 'test_store')
        shopping_list = ShoppingList.query.filter_by(title='test_title').first()
        item = Item.query.filter_by(id=1).first()

        res = shopping_service.add_item_to_shopping_list(shopping_list, item, 1)
        self.assertTrue(res is not None)

    def test_delete_shopping_list(self):
        """
        Unittest : Delete shopping list - success
        :return:
        """
        self.add_shooping_list('test_title', 'test_store')
        shopping_list = ShoppingList.query.filter_by(title='test_title').first()
        item = Item.query.filter_by(id=1).first()
        shopping_service.add_item_to_shopping_list(shopping_list, item, 1)

        res = shopping_service.delete_shopping_list(1)
        self.assertTrue(res == 1)

    def test_delete_shopping_list_fail(self):
        """
        Unittest : Delete shopping list which does not exist - fail
        :return:
        """
        res = shopping_service.delete_shopping_list(1)
        self.assertFalse(res == 1)

    def test_get_all_shopping_list(self):
        """
        Unittest : Get all shopping list - success
        :return:
        """
        self.add_shooping_list('test_title', 'test_store')
        shopping_list = ShoppingList.query.filter_by(title='test_title').first()
        item = Item.query.filter_by(id=1).first()
        shopping_service.add_item_to_shopping_list(shopping_list, item, 1)

        res = shopping_service.get_all_shopping_list()
        self.assertIn('test_title', str(res))
        self.assertIn('Water Bottle', str(res))

    def test_get_all_shopping_list_fail(self):
        """
        Unittest : Get all shopping list when there is none - fail
        :return:
        """
        res = shopping_service.get_all_shopping_list()
        self.assertNotIn('test_title', str(res))
        self.assertNotIn('Water Bottle', str(res))

    def test_get_all_shopping_list_by_title(self):
        """
        Unittest : Get shopping list by title - success
        :return:
        """
        self.add_shooping_list('test_title', 'test_store')
        shopping_list = ShoppingList.query.filter_by(title='test_title').first()
        item = Item.query.filter_by(id=1).first()
        shopping_service.add_item_to_shopping_list(shopping_list, item, 1)

        res = shopping_service.get_shopping_list_by_title('test_title')
        self.assertIn('test_title', str(res))
        self.assertIn('Water Bottle', str(res))

    def test_get_all_shopping_list_by_title_fail(self):
        """
        Unittest : Get shopping list by title when there is none - fail
        :return:
        """
        res = shopping_service.get_shopping_list_by_title('test_title')
        self.assertNotIn('test_title', str(res))
        self.assertNotIn('Water Bottle', str(res))

    def test_search_shopping_list_by_title_keyword(self):
        """
        Unittest : Search shopping list by title containing a keyword - success
        :return:
        """
        self.add_shooping_list('test_title', 'test_store')
        shopping_list = ShoppingList.query.filter_by(title='test_title').first()
        item = Item.query.filter_by(id=1).first()
        shopping_service.add_item_to_shopping_list(shopping_list, item, 1)

        res = shopping_service.search_shopping_list_by_title_keyword('test')
        self.assertIn('test_title', str(res))
        self.assertIn('Water Bottle', str(res))

    def test_search_shopping_list_by_title_keyword_fail(self):
        """
        Unittest : Search shopping list by title containing a keyword - fail
        :return:
        """
        res = shopping_service.search_shopping_list_by_title_keyword('test')
        self.assertNotIn('test_title', str(res))
        self.assertNotIn('Water Bottle', str(res))

    def test_get_shopping_list_by_item_id(self):
        """
        Unittest : Get shopping list by item id - success
        :return:
        """
        self.add_shooping_list('test_title', 'test_store')
        shopping_list = ShoppingList.query.filter_by(title='test_title').first()
        item = Item.query.filter_by(id=1).first()
        shopping_service.add_item_to_shopping_list(shopping_list, item, 1)

        res = shopping_service.get_shopping_list_by_item_id(1)
        self.assertIn('test_title', str(res))
        self.assertIn('Water Bottle', str(res))

    def test_get_shopping_list_by_item_id_fail(self):
        """
        Unittest : Get shopping list by item id - fail
        :return:
        """
        res = shopping_service.get_shopping_list_by_item_id(1)
        self.assertNotIn('test_title', str(res))
        self.assertNotIn('Water Bottle', str(res))

    def test_search_shopping_list_by_item_name_keyword(self):
        """
        Unittest : Search shopping list by item title containing a keyword - success
        :return:
        """
        self.add_shooping_list('test_title', 'test_store')
        shopping_list = ShoppingList.query.filter_by(title='test_title').first()
        item = Item.query.filter_by(id=1).first()
        shopping_service.add_item_to_shopping_list(shopping_list, item, 1)

        res = shopping_service.search_shopping_list_by_item_name_keyword('water')
        self.assertIn('test_title', str(res))
        self.assertIn('Water Bottle', str(res))

    def test_search_shopping_list_by_item_name_keyword_fail(self):
        """
        Unittest : Search shopping list by item title containing a keyword - fail
        :return:
        """
        res = shopping_service.search_shopping_list_by_item_name_keyword('water')
        self.assertNotIn('test_title', str(res))
        self.assertNotIn('Water Bottle', str(res))