"""
Django settings for ordclub project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
import random
import string
import ConfigParser


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# 12 factor config: http://www.wellfireinteractive.com/blog/easier-12-factor-django/
def read_env():
    """Reads local default environment variables from a file.
        <BASE_DIR>/settings.conf
    """
    settings_conf_path = os.path.join(BASE_DIR, 'settings.conf')
    if os.access(settings_conf_path, os.F_OK):
        config = ConfigParser.ConfigParser()
        config.read(settings_conf_path)
        env = config.get('DEFAULT', 'env')
        for key, value in config.items(env):
            os.environ.setdefault(key.upper(), value)

# load env variables from the conf file into settings
read_env()


def env_var(key, default=None, cache=False):
    """Retrieves env vars and makes Python boolean replacements"""
    val = os.environ.get(key, default)
    if cache and val == default:
        os.environ[key] = default
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    return val


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_var('SECRET_KEY',
                     default=''.join(random.choice(string.printable) for x in range(40)))

DEBUG = env_var('DEBUG', default=False)
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = env_var('ALLOWED_HOSTS', default='').split(',')


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'profiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

ROOT_URLCONF = 'ordclub.urls'

WSGI_APPLICATION = 'ordclub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {'default': dj_database_url.config(default='sqlite:///db.sqlite')}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Twitter keys
CONSUMER_KEY = env_var('CONSUMER_KEY')
CONSUMER_SECRET = env_var('CONSUMER_SECRET')
ACCESS_TOKEN_KEY = env_var('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = env_var('ACCESS_TOKEN_SECRET')
