from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Import the configurations
from instance.config import app_config

application = Flask(
        import_name="app",
        template_folder="templates",
        static_folder='static',
        instance_relative_config=True)

database = SQLAlchemy(application)

def create_app(config_name):
    application.config.from_object(app_config[config_name])
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    database.init_app(application)

    migrate = Migrate(app = application, db = database, directory="intron_health_migrations", render_as_batch=True)

    register_blueprints()

    return application


"""
 The following registers the Blueprints with the application.
"""
def register_blueprints():
    # Import all BluePrints
    from .home import home as home_blueprint
    application.register_blueprint(home_blueprint, url_prefix='/home')