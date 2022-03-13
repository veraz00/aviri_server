
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_migrate import Migrate
import os
import base64
import click
from flask import session, g



def fake_images():
    record = dict()
    for file in os.listdir(os.environ['SAMPLE_DIR']):
        record['filename'] = file
        with open(os.path.join(os.environ['SAMPLE_DIR'], file), 'rb') as image1:
            record['content'] = base64.b64encode(image1.read())

            from controller.image import ImageController
            g.image = ImageController()
            g.image.create(record)
    return 


def register_commands(app):
    @app.cli.command()
    @click.option('--images', default=10, help='Quantity of images, default is 20.')
    def forge(images):
        click.echo('Generating the images...')
        fake_images()


from flask_session import Session


db = SQLAlchemy()
DB_NAME = 'db.sqlite3'

def create_database(application):
    db_filename = DB_NAME
    if not os.path.exists(db_filename):
        db.create_all(app=application)
        print('Created database successfully')
        
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 0
    db.init_app(app)
    Session(app)  #  session load the config values from flask application config
    module = import_module('app.api.routes')
    app.register_blueprint(module.blueprint)
    
    Migrate(app, db)
    create_database(app)
    register_commands(app)
                
    return app









