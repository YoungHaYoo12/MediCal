import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  MAIL_SERVER = 'smtp.googlemail.com'
  MAIL_PORT = 587
  MAIL_USE_TLS = True
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  MAIL_SUBJECT_PREFIX = '[MediCal]'
  MAIL_SENDER = 'MediCal Admin <sparkyyoo1212@gmail.com>'

  @staticmethod
  def init_app(app):
    pass

class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data-dev.sqlite')

class TestingConfig(Config):
  TESTING = True
  WTF_CSRF_ENABLED = False
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data-test.sqlite')

class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data.sqlite')

config = {
  'development' : DevelopmentConfig,
  'testing': TestingConfig,
  'production': ProductionConfig,
  'default': DevelopmentConfig
}