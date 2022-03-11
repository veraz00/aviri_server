import os 
class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    
    SQLACHEMY_TRACK_MODICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    IMAGE_FOLDER = os.path.join(basedir, "data")  # current: /Users/zenglinlin/Dev/linlin-server/run.py
class ProductionConfig(Config):
    DEBUG = False
    
class DebugConfig(Config):
    DEBUG = True
    
config_dict = {'Production': ProductionConfig, 'Debug':DebugConfig}
print('sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db.sqlite3'))