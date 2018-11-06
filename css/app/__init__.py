from flask import Flask, session
from css.config import Config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_misaka import Misaka
from flask_session import Session


app = Flask(__name__)
misaka = Misaka(app, fenced_code=True)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)


from css.app import routes
