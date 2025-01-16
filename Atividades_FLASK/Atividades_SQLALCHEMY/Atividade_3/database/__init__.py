from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from .config import Config

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
