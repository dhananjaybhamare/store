import os
from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import Item, UnitMeasurement, ShoppingList, ShoppingListItems


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Item=Item, UnitMeasurement=UnitMeasurement, ShoppingList=ShoppingList,
                ShoppingListItems=ShoppingListItems)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    UnitMeasurement.insert_unit_measurement()

    Item.insert_items()

