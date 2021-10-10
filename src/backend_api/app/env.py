import os

DEFAULT_ROOT = '/app/' if os.path.isfile('/app/main.py') else os.getcwd() + '/'
ROOT_DIR = os.getenv('ROOT_DIR', DEFAULT_ROOT)


DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE'))


PYTEST_MODE = os.getenv('PYTEST_MODE') == 'TRUE'
