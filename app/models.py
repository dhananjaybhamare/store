from . import db
from datetime import datetime


Units = ['EACH', 'PACK']


class UnitMeasurement(db.Model):
    """Database mapping class for Unit Measurement"""
    __tablename__ = 'unit_measurement'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))

    @staticmethod
    def insert_unit_measurement():
        """
        Method to add unit measurements when the application is deployed first time
        :return: void
        """
        unit_measurements = UnitMeasurement.query.first()
        if unit_measurements is None:
            for unitTitle in Units:
                unit = UnitMeasurement(title=unitTitle)
                db.session.add(unit)
            db.session.commit()


class ShoppingListItems(db.Model):
    """Database mapping class for many to many relationship between shopping_list and item tables"""
    __tablename__ = 'shopping_list_items'
    shopping_list_id = db.Column(db.Integer, db.ForeignKey('shopping_list.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=0)
    actual_item_price = db.Column(db.Float, default=0)
    discount_percentage = db.Column(db.Float, default=0)
    discount_per_item = db.Column(db.Float, default=0)
    discounted_item_price = db.Column(db.Float, default=0)
    actual_total_price = db.Column(db.Float, default=0)
    discounted_total_price = db.Column(db.Float, default=0)


class Item(db.Model):
    """Database maping class for item table"""
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    price = db.Column(db.Float)
    discount_percentage = db.Column(db.Float, default=0)
    unit_measurement_id = db.Column(db.Integer, db.ForeignKey('unit_measurement.id'))
    unit_measurement = db.relationship("UnitMeasurement")

    @staticmethod
    def insert_items():
        """
        Method to add items when the application is deployed first time
        :return: void
        """
        items = Item.query.first()
        if items is None:
            item_1 = Item(title='Water Bottle', price=100, discount_percentage=1, unit_measurement_id=1)
            db.session.add(item_1)
            item_2 = Item(title='Rice 1 KG Bag', price=200, discount_percentage=2, unit_measurement_id=2)
            db.session.add(item_2)
            item_3 = Item(title='Energy Drink', price=300, discount_percentage=3, unit_measurement_id=1)
            db.session.add(item_3)
            item_4 = Item(title='Rice 2 KG Bag', price=400, discount_percentage=4, unit_measurement_id=2)
            db.session.add(item_4)
            item_5 = Item(title='Soap', price=500, discount_percentage=5, unit_measurement_id=1)
            db.session.add(item_5)
            item_6 = Item(title='Sugar 1 KG Bag', price=600, discount_percentage=6, unit_measurement_id=2)
            db.session.add(item_6)
            item_7 = Item(title='Tooth Paste', price=700, discount_percentage=7, unit_measurement_id=1)
            db.session.add(item_7)
            item_8 = Item(title='Ice Cream 1 Liter Pack', price=800, discount_percentage=8, unit_measurement_id=2)
            db.session.add(item_8)
            item_9 = Item(title='Notebook', price=900, discount_percentage=9, unit_measurement_id=1)
            db.session.add(item_9)
            item_10 = Item(title='Oranges 1 KG Bag', price=1000, discount_percentage=10, unit_measurement_id=2)
            db.session.add(item_10)
            item_11 = Item(title='Pen', price=1100, discount_percentage=11, unit_measurement_id=1)
            db.session.add(item_11)
            item_12 = Item(title='Apple 1 KG Bag', price=1200, discount_percentage=12, unit_measurement_id=2)
            db.session.add(item_12)
            db.session.commit()


class ShoppingList(db.Model):
    """Database mapping class for shopping_list table"""
    __tablename__ = 'shopping_list'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    store_name = db.Column(db.String(64))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow)
