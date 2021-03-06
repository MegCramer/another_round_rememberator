from flask import Flask
from .config import CONFIG_VARS

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{0}:{1}@{2}/{3}"\
            .format(CONFIG_VARS['DB_USER'], CONFIG_VARS['DB_PW'], CONFIG_VARS['DB_HOST'], CONFIG_VARS['DB_NAME'])
    app.config['SECRET_KEY'] = config.CONFIG_VARS['SECRET_KEY']
    app.config['DEBUG'] = True if config.CONFIG_VARS['DEBUG'] == 'True' else False

    return app
