from app.models import ShoppingList, Item, ShoppingListItems
from app import db


def add_shopping_list(title, store_name):
    """
    This methos will add a new shopping list.
    If shopping list already exist then will return null
    :param title:
    :param store_name:
    :return: shopping_list_id
    """
    shopping_list = ShoppingList.query.filter_by(title=title, store_name=store_name).first()
    if shopping_list is None:
        shopping_list = ShoppingList(title=title, store_name=store_name)
        db.session.add(shopping_list)
        db.session.commit()
    else:
        return ""
    return shopping_list.id


def update_shopping_list(shopping_list_id, title, store_name):
    """
    This method updates title/store_name of the shopping list.
    :param shopping_list_id:
    :param title:
    :param store_name:
    :return: shopping_list_id
    """
    shopping_list = ShoppingList.query.filter_by(id=shopping_list_id).first()
    if shopping_list is not None:
        if title:
            shopping_list.title = title
        if store_name:
            shopping_list.store_name = store_name
        db.session.add(shopping_list)
        db.session.commit()
    else:
        return ""
    return shopping_list_id


def get_item(item_id):
    """
    This method retrieve the Item and returns the same.
    :param item_id:
    :return: Item
    """
    return Item.query.filter_by(id=item_id).first()


def get_shopping_list(shopping_list_id):
    """
    This methos retrieve the ShoppingList and returns the same.
    :param shopping_list_id:
    :return: ShoppingList
    """
    return ShoppingList.query.filter_by(id=shopping_list_id).first()


def add_item_to_shopping_list(shopping_list, item, quantity):
    """
    This method item with given quantity in the shopping list.
    :param shopping_list:
    :param item:
    :param quantity:
    :return: data
    """
    shopping_list_items = ShoppingListItems.query.filter_by(shopping_list_id=shopping_list.id, item_id=item.id).first()
    if shopping_list_items is None:
        shopping_list_items = ShoppingListItems(shopping_list_id=shopping_list.id, item_id=item.id,
                                                discount_percentage=item.discount_percentage,
                                                actual_item_price=item.price,
                                                quantity=0)
        shopping_list_items.discount_per_item = \
            shopping_list_items.actual_item_price * shopping_list_items.discount_percentage / 100
        shopping_list_items.discounted_item_price = \
            shopping_list_items.actual_item_price - shopping_list_items.discount_per_item

    shopping_list_items.quantity += quantity
    shopping_list_items.actual_total_price = shopping_list_items.actual_item_price * shopping_list_items.quantity
    shopping_list_items.discounted_total_price = \
        shopping_list_items.discounted_item_price * shopping_list_items.quantity

    db.session.add(shopping_list_items)
    db.session.commit()

    all_shopping_list_items = ShoppingListItems.query.filter_by(shopping_list_id=shopping_list.id).all()
    all_items = []
    for shopping_list_item in all_shopping_list_items:
        item = Item.query.filter_by(id=shopping_list_item.item_id).first()
        item_data = {
            "item_title": item.title,
            "actual_item_price": shopping_list_item.actual_item_price,
            "discount_percentage": shopping_list_item.discount_percentage,
            "discounted_item_price": shopping_list_item.discounted_item_price,
            "quantity": shopping_list_item.quantity,
            "actual_total_price": shopping_list_item.actual_total_price,
            "discounted_total_price": shopping_list_item.discounted_total_price
        }
        all_items.append(item_data)

    data = {
        "shopping_list_title": shopping_list.title,
        "store_name": shopping_list.store_name,
        "items": all_items
    }
    return data


def delete_shopping_list(shopping_list_id):
    """
    This method delete the shopping list and items added to the shopping list
    :param shopping_list_id:
    :return:
    """
    shopping_list_items = ShoppingListItems.query.filter_by(shopping_list_id=shopping_list_id).all()
    shopping_list = ShoppingList.query.filter_by(id=shopping_list_id).first()
    if shopping_list is not None:
        if shopping_list_items is not None:
            for item in shopping_list_items:
                db.session.delete(item)
        db.session.delete(shopping_list)
        db.session.commit()
    else:
        return ""
    return shopping_list_id
