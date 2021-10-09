import os

DEFAULT_ROOT = '/app/' if os.path.isfile('/app/main.py') else os.getcwd() + '/'
ROOT_DIR = os.getenv('ROOT_DIR', DEFAULT_ROOT)

PYTEST_MODE = os.getenv('PYTEST_MODE') == 'TRUE'
