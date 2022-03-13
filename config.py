import os 
class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))  # aviri_server
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    BOOTSTRAP_SERVE_LOCAL = True
    SQLACHEMY_TRACK_MODICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    IMAGE_FOLDER = os.path.join(basedir, "input")  # current: /Users/zenglinlin/Dev/linlin-server/run.py
class ProductionConfig(Config):
    DEBUG = False
    
class DebugConfig(Config):
    DEBUG = True
    
config_map = {'Production': ProductionConfig, 'Debug':DebugConfig}
