from .base import *
from django_ecommerce.config.utils import get_file_secret


DEBUG = False

POSTGRES_USER = get_file_secret(os.getenv('POSTGRES_USER_FILE'))
POSTGRES_PASSWORD = get_file_secret(os.getenv('POSTGRES_PASSWORD_FILE'))

DATABASES['default']['HOST'] = os.getenv('POSTGRES_HOST')
DATABASES['default']['USER'] = POSTGRES_USER
DATABASES['default']['PASSWORD'] = POSTGRES_PASSWORD
