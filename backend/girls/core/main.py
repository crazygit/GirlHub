import importlib
import os

from flask import Flask, Blueprint

from girls.config import dev
from .extensions import db, cors
from girls.apis import api


def app_factory(config=None):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app = Flask(__name__,
                static_folder=os.path.join(root_dir, 'static'),
                template_folder=os.path.join(root_dir, 'templates'))
    config_app(app, config or dev)
    config_database(app)
    config_url_rule(app)
    config_blueprints(app)
    # config_logger(app)
    app.logger.info("app started ...")
    if app.debug:
        print_url_map(app)
    return app


def print_url_map(app):
    for url in app.url_map.iter_rules():
        app.logger.debug(url)


def config_blueprints(app):
    api_blueprint = Blueprint('api', __name__)
    api.init_app(api_blueprint)
    image_blueprint = Blueprint('image', __name__,
                                static_folder=app.config['IMAGES_STORE'])
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    app.register_blueprint(image_blueprint, url_prefix='/image')
    # enable cors when debug
    if app.debug:
        cors.init_app(app, resources=r'/api/v1/*')


def config_url_rule(app):
    def index():
        return 'Building'

    app.add_url_rule('/', 'index', index)


# def config_logger(app, force=False):
#     if force or not app.debug:
#         stream_format = logging.Formatter(
#             '%(asctime)s %(name)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
#         stream_handler = logging.StreamHandler()
#         stream_handler.setFormatter(stream_format)
#         stream_handler.setLevel(logging.INFO)
#
#         app.logger.addHandler(stream_handler)
#         app.logger.setLevel(logging.INFO)


def config_app(app, config):
    if isinstance(config, str):
        config = importlib.import_module('girls.config.%s' % config)
    app.config.from_object(config)


def config_database(app):
    db.init_app(app)
    db.app = app
    db.create_all()
