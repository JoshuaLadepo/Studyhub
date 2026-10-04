import os
from pathlib import Path

from flask import Flask
from dotenv import load_dotenv
from extensions import db
from routes import routes

env_path = Path(__file__).with_name(".env")
load_dotenv(env_path)

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL was not loaded")

def create_app(database_uri = None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri or database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(routes)
    
    return app

app = create_app()






if __name__ == "__main__":
    app.run(debug=True)