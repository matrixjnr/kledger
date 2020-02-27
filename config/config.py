import os
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    DEBUG = True
    CSRF_ENABLED = True


class Configdb():
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'kledger_test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://xdkqznupmgnkdg:cfa95b4e85f17bb2df9d1af784acc694670cf4bd6a1a5b22ba58faa324a4eef8@ec2-3-213-192-58.compute-1.amazonaws.com:5432/ddrf7lcrug4tpi'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
