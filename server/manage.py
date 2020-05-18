import os

from flask import Flask
from flask_cors import CORS
from flask_script import Manager

from main.config import config_by_name
from main import main_bp

def create_app(config_name):
    app = Flask(__name__)
    cfg = config_by_name[config_name]

    app.config.from_object(cfg)
    app.register_blueprint(main_bp)
    print(cfg)

    CORS(app, resources=cfg.CORS)
    return app

app = create_app(os.getenv("FLASK_ENV", "dev"))
manager = Manager(app)


@manager.command
def prod():
    app.run(debug=False, host="0.0.0.0", port=5000)

@manager.command
def dev():
    app.run(debug=True, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    manager.run()