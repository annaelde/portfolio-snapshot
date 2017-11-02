import json
from .base import *

secretFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'production.json')
with open(secretFile) as f:
    secrets = json.loads(f.read())

SECRET_KEY = get_secret('SECRET_KEY', secrets)
SITE_ID = 3

DEBUG = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

MEDIA_ROOT = get_secret('MEDIA_ROOT', secrets)
STATIC_ROOT = get_secret('STATIC_ROOT', secrets)

GOOGLE_RECAPTCHA_SECRET_KEY = get_secret('RECAPTCHA_KEY_SECRET', secrets)
GOOGLE_RECAPTCHA_PUBLIC_KEY = get_secret('RECAPTCHA_KEY_PUBLIC', secrets)

TWITTER_CONSUMER = get_secret('TWITTER_CONSUMER', secrets)
TWITTER_CONSUMER_SECRET = get_secret('TWITTER_CONSUMER_SECRET', secrets)
TWITTER_ACCESS = get_secret('TWITTER_ACCESS', secrets)
TWITTER_ACCESS_SECRET = get_secret('TWITTER_ACCESS_SECRET', secrets) 

ALLOWED_HOSTS = get_secret('ALLOWED_HOSTS', secrets)
DATABASES = {
    'default': get_secret('DATABASE_CONFIG', secrets)
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_secret('EMAIL_HOST', secrets)
EMAIL_HOST_USER = get_secret('EMAIL_USER', secrets)
EMAIL_HOST_PASSWORD = get_secret('EMAIL_PASSWORD', secrets)
EMAIL_PORT = get_secret('EMAIL_PORT', secrets)
PERSONAL_EMAIL = get_secret('PERSONAL_EMAIL', secrets)
EMAIL_USE_TLS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': get_secret('DJANGO_LOG', secrets),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
