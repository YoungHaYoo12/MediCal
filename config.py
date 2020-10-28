import os
from dotenv import find_dotenv, load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config():
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  @staticmethod
  def init_app(app):
    pass

class ProductionConfig(Config):
  DEBUG = False

class TestingConfig(Config):
  TESTING = True
  WTF_CSRF_ENABLED = False


config = {
  'testing': TestingConfig,
  'default': ProductionConfig
}
