
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_migrate import Migrate
import os
import base64
import click
from flask import session, g
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
    db.init_app(app)
    Session(app)  #  session load the config values from flask application config
    module = import_module('app.api.routes')
    app.register_blueprint(module.blueprint)
    
    Migrate(app, db)
    create_database(app)
    register_commands(app)
                
    return app









