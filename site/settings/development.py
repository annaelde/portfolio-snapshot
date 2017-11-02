import json
from .base import *

secretFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'development.json')

with open(secretFile) as f:
    secrets = json.loads(f.read())

SECRET_KEY = get_secret('SECRET_KEY', secrets)
DEBUG = True
SITE_ID = 2

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

GOOGLE_RECAPTCHA_SECRET_KEY = get_secret('RECAPTCHA_KEY_SECRET', secrets)
GOOGLE_RECAPTCHA_PUBLIC_KEY = get_secret('RECAPTCHA_KEY_PUBLIC', secrets)

TWITTER_CONSUMER = ''
TWITTER_CONSUMER_SECRET = ''
TWITTER_ACCESS = ''
TWITTER_ACCESS_SECRET = ''

ALLOWED_HOSTS = get_secret('ALLOWED_HOSTS', secrets)
DATABASES = {
    'default': get_secret('DATABASE_CONFIG', secrets)
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/aec/temp/email'
PERSONAL_EMAIL = get_secret('PERSONAL_EMAIL', secrets)
EMAIL_USE_TLS = False
