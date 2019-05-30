from __future__ import absolute_import, unicode_literals
import os
from .settings import *
import dj_database_url


env = os.environ.copy()
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')

DEBUG = False
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*',]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
