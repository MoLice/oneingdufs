# coding=utf-8
"""oneingdufs.settings 项目设置文件"""

import os.path
from os import environ

# 自定义变量
PRO_PATH = os.path.dirname(__file__) # 项目的绝对路径

# 项目的登录退出url
LOGIN_URL = '/home/login/'
LOGOUT_URL = '/home/logout/'
# 登录成功且url不带有next查询字符串时的跳转url
LOGIN_REDIRECT_URL = '/home/'

################
# LOCAL or SAE #
################

isSAE = environ.get("APP_NAME", "")
if isSAE:
  # SAE
  import sae.const
  
  DEBUG = True

  # database
  MYSQL_DB = sae.const.MYSQL_DB 
  MYSQL_USER = sae.const.MYSQL_USER 
  MYSQL_PASS = sae.const.MYSQL_PASS 
  MYSQL_HOST_M = sae.const.MYSQL_HOST 
  MYSQL_HOST_S = sae.const.MYSQL_HOST_S 
  MYSQL_PORT = sae.const.MYSQL_PORT
else:
  # LOCAL

  DEBUG = True

  # static
  STATIC_URL = 'http://localhost/static/'
  STATIC_ROOT = os.path.join(PRO_PATH, '..', 'static')

  # database
  MYSQL_DB = 'oneingdufs'
  MYSQL_USER = 'root'
  MYSQL_PASS = '123'
  MYSQL_HOST_M = 'localhost'
  MYSQL_HOST_S = 'localhost'
  MYSQL_PORT = '3306'

### endif isSAE ###

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('MoLice', 'sf.molice@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': MYSQL_DB,                      # Or path to database file if using sqlite3.
        'USER': MYSQL_USER,                      # Not used with sqlite3.
        'PASSWORD': MYSQL_PASS,                  # Not used with sqlite3.
        'HOST': MYSQL_HOST_M,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': MYSQL_PORT,                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z8dmkszmsqo%n4)+$kgl^)um^hdso#ps80qot$b+(33wkk39pk'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',#POST CSRF ERROR
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'oneingdufs.urls'

TEMPLATE_DIRS = (
    os.path.join(PRO_PATH, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    #'django.core.context_processors.debug',
    #'django.core.context_processors.i18n',
    #'django.core.context_processors.media',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',

    'oneingdufs.administration',
    'oneingdufs.personalinfo',
    'oneingdufs.campuscard',
    'oneingdufs.home',
)
