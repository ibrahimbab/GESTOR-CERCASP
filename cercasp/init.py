from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api
from flask_babel import Babel
from apscheduler.schedulers.background import BackgroundScheduler
from cryptography.fernet import Fernet
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)
api = Api()
babel = Babel()
scheduler = BackgroundScheduler()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Logging
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    limiter.init_app(app)
    api.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    # Encriptación
    global fernet
    fernet = Fernet(app.config['ENCRYPTION_KEY'])

    # Registrar blueprints
    from .blueprints.auth import auth_bp
    from .blueprints.dashboard import dashboard_bp
    from .blueprints.interns import interns_bp
    from .blueprints.payments import payments_bp
    from .blueprints.progress import progress_bp
    from .blueprints.inventory import inventory_bp
    from .blueprints.reports import reports_bp
    from .blueprints.api import api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(interns_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(api_bp)

    # Scheduler
    from .utils import backup_db
    from .ml_model import train_model
    scheduler.add_job(train_model, 'interval', hours=12)
    scheduler.add_job(backup_db, 'interval', days=1)
    scheduler.start()

    with app.app_context():
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])
