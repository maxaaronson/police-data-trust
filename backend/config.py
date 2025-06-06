import os
from dotenv import load_dotenv
from datetime import timedelta
if os.environ.get("FLASK_ENV") != "production":
    load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(32))
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", os.urandom(64))
    JWT_TOKEN_LOCATION = os.environ.get(
        "JWT_TOKEN_LOCATION", ["headers", "cookies"]
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    TOKEN_EXPIRATION = timedelta(
        hours=os.environ.get("TOKEN_EXPIRATION_HOURS", 12)
    )
    GRAPH_USER = os.environ.get("GRAPH_USER", "neo4j")
    GRAPH_NM_URI = os.environ.get("GRAPH_NM_URI", "localhost:7687")
    GRAPH_PASSWORD = os.environ.get("GRAPH_PASSWORD", "password")
    GRAPH_DB = os.environ.get("GRAPH_DB", "police_data")

    # Flask-Mail SMTP server settings
    """
    Config settings for email sending
    Put all of the information in your dotenv
    config file
    """
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "false").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER",
        "National Police Data Coalition <{email}>".format(
              email=MAIL_USERNAME),
    )
    FRONT_END_URL = os.environ.get("FRONT_END_URL")

    """
    Testing configurations with Mailtrap Email testing, all the configurations
    will be different--go to mailtrap for more information
    """
    # MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    # MAIL_PORT = 2525
    # MAIL_USERNAME = '30a682ceaa0416'
    # MAIL_PASSWORD = 'dbf502527604b1'
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False

    # Flask-User settings
    USER_APP_NAME = (
        "Police Data Trust"  # Shown in and email templates and page footers
    )
    USER_ENABLE_EMAIL = True  # Enable email authentication
    USER_ENABLE_USERNAME = True  # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@policedatatrust.com"

    FRONTEND_PORT = os.environ.get("NPDI_WEB_PORT", "3000")
    FRONTEND_URL = os.environ.get(
        "FRONTEND_URL",
        "http://localhost:" + FRONTEND_PORT
    )

    SCRAPER_SQS_QUEUE_NAME = os.environ.get("SCRAPER_SQS_QUEUE_NAME")

    @property
    def NEO4J_BOLT_URI(self):
        return "bolt://{user}:{pw}@{uri}".format(
            user=self.GRAPH_USER,
            pw=self.GRAPH_PASSWORD,
            uri=self.GRAPH_NM_URI
        )

    @property
    def MIXPANEL_TOKEN(self):
        return os.environ.get("MIXPANEL_TOKEN", None)


class DevelopmentConfig(Config):
    ENV = "development"
    # Use fixed secrets in development so tokens work across server restarts
    SECRET_KEY = os.environ.get("SECRET_KEY", "my-secret-key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "my-jwt-secret-key")


class ProductionConfig(Config):
    """Config designed for Heroku CLI deployment."""

    ENV = "production"
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True

    # @property
    # def SQLALCHEMY_DATABASE_URI(self):
    #     return os.environ.get("DATABASE_URL")


class TestingConfig(Config):
    ENV = "testing"
    TESTING = True
    GRAPH_DB = "police_data_test"
    GRAPH_NM_URI = os.environ.get("GRAPH_TEST_URI", "test-neo4j:7687")
    GRAPH_USER = "neo4j"
    GRAPH_PASSWORD = "test_pwd"
    SECRET_KEY = "my-secret-key"
    JWT_SECRET_KEY = "my-jwt-secret-key"
    MIXPANEL_TOKEN = "mixpanel-token"


def get_config_from_env(env: str) -> Config:
    """This function takes a string variable, looks at what that string variable
    is, and returns an instance of a Config class corresponding to that string
    variable.

    Args:
        env: (str) A string. Usually this is from `app.env` in the
             `create_app` function, which in turn is set by the environment
             variable `FLASK_ENV`.
    Returns:
        A Config instance corresponding with the string passed.

    Example:
        >>> get_config_from_env('development')
        DevelopmentConfig()
    """
    config_mapping = {
        "production": ProductionConfig,
        "development": DevelopmentConfig,
        "testing": TestingConfig,
    }
    try:
        config = config_mapping[env]
    except KeyError:
        print(
            f"Bad config passed."
            f"The config must be in {config_mapping.keys()}"
        )
        raise
    else:
        return config()
