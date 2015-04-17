"""
Django settings for webops project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%aa-kwa8-brq%a^r+&9ct5pujksr_1gu84teiz@i3cm_%bva3t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'debug_toolbar',
    'django_rq',

    'webops_django',
    'geoops',
    'opstest',
    'imageops',
    #'gitops',
    
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    

)

ROOT_URLCONF = 'webops.urls'

WSGI_APPLICATION = 'webops.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


if DEBUG:
    STATICFILES_DIRS = (
        os.path.abspath(os.path.join(BASE_DIR, "../statics/webops")),
    )

CORS_ORIGIN_ALLOW_ALL = True



## GIT BASED CONFIGURATION ... WORK IN PROGRESS ...
#GITOPS_BASE_CACHE = os.path.join(BASE_DIR, "gitops_cache")
#GITOPS_REMOTE_OPS = [ "https://github.com/bianchimro/remote-op-test.git"]

#this is the default
WEBOPS_BREAK_ON_FAIL_TEST = False

WEBOPS_OPS = [
    { "op_class" : "opstest.ops.DummyOp"}, 
    { "op_class" : "opstest.ops.SumOp"}, 
    {'op_graph' : os.path.join(BASE_DIR, 'opstest', 'convert_to_tiff.json')},
    {'op_graph' : os.path.join(BASE_DIR, 'opstest', 'sum_and_sum10.json')},
    {'op_graph' : os.path.join(BASE_DIR, 'opstest', 'sum_and_sum10_again.json')}
]


RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0
    }
    
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'webops_django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}