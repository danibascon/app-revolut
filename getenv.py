import os

MONGO_INITDB_ROOT_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME') or 'revolut'
MONGO_INITDB_ROOT_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD') or 'revolut'
MONGO_INITDB_HOST_NAME = os.getenv('MONGO_INITDB_HOST_NAME') or 'ddbb'
