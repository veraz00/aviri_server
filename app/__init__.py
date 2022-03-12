from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from flask_migrate import Migrate
from importlib import import_module
from flask_session import Session
import os 
import base64
import click
import os 


from flask_bootstrap import Bootstrap
bootstrap = Bootstrap()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

import sys, os
print(os.getcwd())
def register_extensions(app):
    bootstrap.init_app(app)  # bootstrap??
    db.init_app(app)
    from flask_session import Session
    Session(app)  #  session load the config values from flask application config
    Migrate(app, db)


def fake_images():
    # db.drop_all()
    db.create_all()
    record = dict()
    for file in os.listdir(os.environ['SAMPLE_DIR']):
        record['filename'] = file
        with open(os.path.join(os.environ['SAMPLE_DIR'], file), 'rb') as image1:
            record['content'] = base64.b64encode(image1.read())

            from controller.image import ImageController
            g.image = ImageController()
            img = g.image.create(record)
    return 


def register_commands(app):
    @app.cli.command()
    @click.option('--images', default=10, help='Quantity of images, default is 20.')
    def forge(images):
        click.echo('Generating the images...')
        fake_images()

  

def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)
    module = import_module('app.api.routes')
    app.register_blueprint(module.blueprint)
    register_extensions(app)
    register_commands(app)
    
    from app import models

    # db.create_all(app=app)


    return app
