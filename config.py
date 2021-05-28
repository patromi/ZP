import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = 'SensoPark'
    MAIL_SENDER = 'Serwis SensoPark'
    ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CAPTCHA_ENABLE = True
    CAPTCHA_LENGTH = 5
    CAPTCHA_WIDTH = 160
    CAPTCHA_HEIGHT = 60
    SESSION_TYPE = 'sqlalchemy'
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD')
    SQL_IP = os.environ.get('SQL_IP')
    SQL_DB = os.environ.get('SQL_DB')
    SQL_NAME = os.environ.get('SQL_NAME')
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{Config.SQL_NAME}:{Config.SQL_PASSWORD}@{Config.SQL_IP}/{Config.SQL_DB}'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{Config.SQL_NAME}:{Config.SQL_PASSWORD}@{Config.SQL_IP}/{Config.SQL_DB}'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{Config.SQL_NAME}:{Config.SQL_PASSWORD}@{Config.SQL_IP}/{Config.SQL_DB}'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}