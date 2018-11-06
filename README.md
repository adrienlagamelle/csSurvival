# csSurvival

1. Installation
    1. Create a python virtual environment  
        `python3 -m venv venv`
    2. Enter virtual environment  
        `source venv/bin/activate`
    3. Install csSociety egg using pip  
        `pip install css.tar.gz`
    4. Install WhooshAlchemy from git  
        `pip install git+git://github.com/miguelgrinberg/flask-whooshalchemy.git`


2. Running
    1. Set flask app  **replace python3.5 with your version of python**
        `export FLASK_APP=venv/lib/python3.5/site-packages/css/css.py`
    2. Initialize the database
        ```
        flask db init
        flask db migrate
        flask db upgrade
        ```
    2. Run flask  
        `flask run`
