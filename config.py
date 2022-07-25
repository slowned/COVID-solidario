from os import environ

class BaseConfig(object):
    """Base configuration."""

    DEBUG = None
    DB_HOST = "bd_name"
    DB_USER = "db_user"
    DB_PASS = "db_pass"
    DB_NAME = "db_name"
    SECRET_KEY = "secret"

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    ENV = "development"
    DEBUG = environ.get("DEBUG", True)
    SQLALCHEMY_ECHO = True
    SECRET_KEY = 'p9Bv<3Eid9%$i01'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:admin@localhost/centros'
    EXPLAIN_TEMPLATE_LOADING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # to fix error ??

class TestingConfig(BaseConfig):
    """Testing configuration."""

    ENV = "testing"
    TESTING = True
    DEBUG = environ.get("DEBUG", True)
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "admin")
    DB_PASS = environ.get("DB_PASS", "admin")
    DB_NAME = environ.get("DB_NAME", "centros")


class ProductionConfig(BaseConfig):
    """Production configuration."""

    ENV = "production"
    DEBUG = environ.get("DEBUG", False)
    # DB_HOST = environ.get("DB_HOST", "localhost")
    # DB_USER = environ.get("DB_USER", "centros")
    # DB_PASS = environ.get("DB_PASS", "NTNkMzM3NGUxYjdm")
    # DB_NAME = environ.get("DB_NAME", "centros")
    SECRET_KEY = 'p9Bv<3Eid9%$i01'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://centros:NTNkMzM3NGUxYjdm@127.0.0.1/centros'


CONFIG = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
)
