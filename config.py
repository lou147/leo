class Config(object):
    """Base config class."""
    SECRET_KEY = 'takeiteazy'


class ProdConfig(Config):
    """Production config class."""
    pass


class DevConfig(Config):
    """Development config class."""
    # Open the DEBUG
    DEBUG = True
    ASSETS_DEBUG = True

    CACHE_TYPE = 'simple'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/blog'  # mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]

