from __future__ import absolute_import, unicode_literals
import os
from .settings import *
import dj_database_url
# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = '*zah4_+4+0@uhn60h9krn1!on^_knex-rh=z*)nk4_^y=2dy*b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
