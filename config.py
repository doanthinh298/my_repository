import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    RUN_SETTING = {
        'host': os.environ.get('SERVER_HOST', 'localhost'),
        'port': int(os.environ.get('SERVER_PORT', 8080)),
        'debug': os.getenv('DEBUG', False),
        "access_log": False,
        "auto_reload": True,
        'workers': int(os.getenv('SERVER_WORKERS', 4))
    }
    # uWSGI를 통해 배포되어야 하므로, production level에선 run setting을 건드리지 않음
    FALLBACK_ERROR_FORMAT = 'json'

    OAS_UI_DEFAULT = 'swagger'
    SWAGGER_UI_CONFIGURATION = {
        'apisSorter': "alpha",
        'docExpansion': "list",
        'operationsSorter': "alpha"
    }

    SECRET_KEY = os.getenv('SECRET_KEY', 'example project')
    EXPIRATION_JWT = 2592000  # 1 month

    SERVER_NAME = os.getenv('SERVER_NAME')

class LocalDBConfig:
    pass


class RemoteDBConfig:
    pass

class Database:
    USERNAME = os.environ.get("MONGO_USERNAME") or "just_for_dev"
    PASSWORD = os.environ.get("MONGO_PASSWORD") or "password_for_dev"
    HOST = os.environ.get("MONGO_HOST") or "localhost"
    PORT = os.environ.get("MONGO_PORT") or "27017"
    DATABASE = os.environ.get("MONGO_DATABASE") or "example_db"
