from flask import Flask
from api.v1.user_routes import user_blueprint
from config.config import Config
from flask_migrate import Migrate
from models import db

app = Flask(__name__)

def create_app():
    app.config.from_object(Config)

    db.init_app(app)  # Initialize the database

    # Initialize migration
    Migrate(app, db)

    # Register blueprints for routes
    app.register_blueprint(user_blueprint, url_prefix='/api/v1/user')

    return app

create_app()

if __name__ == "__main__":
    app.run(debug=True)
