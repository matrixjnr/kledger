from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from config.config import Configdb, Config


app = Flask(__name__)
app.config.from_object(Config)
app.config.from_object(Configdb)


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
