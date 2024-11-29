from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models here
from .user import User