from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from config.config import DevelopmentConfig


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
