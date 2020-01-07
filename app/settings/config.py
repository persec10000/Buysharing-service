import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:''@127.0.0.1:3306/buysharing_new'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ben:Ben0102%40@159.65.13.232:3306/buysharing_new'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ben:Ben0102%40@localhost:3306/buysharing_new'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Noi12345@@localhost:3306/buysharing_new'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
