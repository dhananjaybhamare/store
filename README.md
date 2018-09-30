# Flask-restful api
Online store shopping list restful apis

## How to run the app
* If you wish to run your own build, first ensure you have python3.6 globally installed in your computer. If not, you can get python3 [here](https://www.python.org).
* After this clone this repository on your machine
* Open command prompt and navigate to store directory
* Create a virtual environment
    ```
        $ python -m venv venv
    ```
* Activate your virtual environment
    ```
    Windows
        $ venv\Scripts\activate
    Mac
        $ venv/bin/activate
    ```
* Install requirements
    ```
        $ pip install -r requirements/dev.txt
    ```
* Set the flask application and environment
    ```
    Windows
        $ set FLASK_APP=store.py
        $ set FLASK_ENV=development
    Mac
        $ export FLASK_APP=store.py
        $ export FLASK_ENV=development
    ```
* Do database migration
    ```
        $ flask deploy
    ```
* Run app
    ```
        $ flask run
    ```

## How to run unit test and check coverage
* Set the flask application and environment
    ```
    Windows
        $ set FLASK_APP=store.py
        $ set FLASK_ENV=testing
    Mac
        $ export FLASK_APP=store.py
        $ export FLASK_ENV=testing
    ```
* Run tests
    ```
        $ flask test --coverage
    ```
* Open store/tmp/coverage/index.html file to refer test coverage

## Refernces
* [Setting Up a Flask Application in PyCharm](https://blog.miguelgrinberg.com/post/setting-up-a-flask-application-in-pycharm)
* [Flask Tutorials](http://flask.pocoo.org/docs/1.0/tutorial/)
* [Flask Restful Tutorials](https://flask-restful.readthedocs.io/en/latest/)
* [SQLAlchemy 1.2 Documentation](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html)
* [Unittest](https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way)
* Stackoverflow discussion forum  
