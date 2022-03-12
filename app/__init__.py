
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_migrate import Migrate
import os
import base64
import click
from flask import session, g

db = SQLAlchemy()

def register_extensions(app):
    db.init_app(app)

def register_blueprints(app):

    module = import_module('app.api.routes')
    app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        print("before_request is running!")
        db.create_all()
        record = dict()
        for file in os.listdir(os.environ['SAMPLE_DIR']):
            record['filename'] = file
            with open(os.path.join(os.environ['SAMPLE_DIR'], file), 'rb') as image1:
                record['content'] = base64.b64encode(image1.read())

                from controller.image import ImageController
                g.image = ImageController()
                g.image.create(record)
        return 


    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


# def fake_images():
#     db.create_all()
#     record = dict()
#     for file in os.listdir(os.environ['SAMPLE_DIR']):
#         record['filename'] = file
#         with open(os.path.join(os.environ['SAMPLE_DIR'], file), 'rb') as image1:
#             record['content'] = base64.b64encode(image1.read())

#             from controller.image import ImageController
#             g.image = ImageController()
#             img = g.image.create(record)
#     return 


# def register_commands(app):
#     @app.cli.command()
#     @click.option('--images', default=10, help='Quantity of images, default is 20.')
#     def forge(images):
#         click.echo('Generating the images...')
#         fake_images()



def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    # register_commands(app)
    Migrate(app, db)
    
    return app







