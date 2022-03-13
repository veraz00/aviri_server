from app import create_app, db
from config import config_map
from flask_migrate import Migrate

app = create_app(config_map['Debug']) 
if __name__ == "__main__":
    print(app)
    app.run(host='0.0.0.0', port = 5050, debug=True, use_reloader=True)
