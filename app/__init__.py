from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import asyncio
from flask import Flask

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
ma = Marshmallow()


def create_app(config_name):
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    toolbar = DebugToolbarExtension(app)
    app.config['SECRET_KEY'] = 'jeabcpis'
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
    app.config['TESTING'] = True
    app.config['DEBUG'] = True

    login_manager.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    from .manager import manager as manager_blueprint
    app.register_blueprint(manager_blueprint, url_prefix='/parking')
    from .reservation import reservation as reservation_blueprint
    app.register_blueprint(reservation_blueprint, url_prefix='/reservation')
    return app


async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")
