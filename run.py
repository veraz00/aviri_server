from app import create_app
from config import config_dict

app = create_app(config_dict['Debug']) 

if __name__ == "__main__":
    print(app)
    app.run(host='0.0.0.0', port = 5050, debug=True)
