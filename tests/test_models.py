import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import Item, ShoppingList, ShoppingListItems, UnitMeasurement


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

    def test_unit_measurement(self):
        unit = UnitMeasurement(title='test_title')
        db.session.add(unit)
        db.session.commit()
        self.assertTrue(UnitMeasurement.query.filter_by(title='test_title').first() is not None)

    def test_item(self):
        item = Item(title='test_title', price=100, discount_percentage=10, unit_measurement_id=1)
        db.session.add(item)
        db.session.commit()
        self.assertTrue(Item.query.filter_by(title='test_title').first() is not None)

    def test__shopping_list(self):
        shopping_list = ShoppingList(title='test_title', store_name='test_store')
        db.session.add(shopping_list)
        db.session.commit()
        self.assertTrue(ShoppingList.query.filter_by(title='test_title').first() is not None)

    def test__shopping_list_item(self):
        shopping_list = ShoppingList(title='test_title', store_name='test_store')
        db.session.add(shopping_list)
        db.session.commit()

        shopping_list_item = ShoppingListItems(shopping_list_id=1, item_id=1, quantity=1, actual_item_price=100,
                                               discount_percentage=10, discount_per_item=10, discounted_item_price=90,
                                               actual_total_price=100, discounted_total_price=90)
        db.session.add(shopping_list_item)
        db.session.commit()

        self.assertTrue(ShoppingListItems.query.filter_by(shopping_list_id=1, item_id=1).first() is not None)
