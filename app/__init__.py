from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from importlib import import_module
from flask_session import Session
import os 

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
    
    module1 = import_module('app.data.routes')
    app.register_blueprint(module1.blueprint)
    create_database(app)
    return app