import os

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


################################################################################
#         Settings most likely to need overriding in local_settings.py         #
################################################################################

# Jasmin telnet defaults, override in local_settings.py
TELNET_HOST = '127.0.0.1'
TELNET_PORT = 8991
TELNET_USERNAME = 'jcliadmin'
TELNET_PW = 'jclipwd'  # no alternative storing as plain text
TELNET_TIMEOUT = 10  # reasonable value for intranet.
JASMIN_HOSTS = [('127.0.0.1', '8991'), ('127.0.0.1', '8992')]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
SECRET_KEY = 'cbuadc$z@xym4j04%b4cf1+w7x!t1*o=%=av(f47^apz#5*+v5'

################################################################################
#                            Other settings                                    #
################################################################################


STANDARD_PROMPT = 'jcli : '  # There should be no need to change this
INTERACTIVE_PROMPT = '> '  # Prompt for interactive commands

# This should be OK for REST API - we are not generating URLs
# see https://www.djangoproject.com/weblog/2013/feb/19/security/#s-issue-host-header-poisoning
ALLOWED_HOSTS = ['*']

SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '',
    'is_authenticated': False,
    'is_superuser': False,
    'info': {
        'description': 'A REST API for managing Jasmin SMS Gateway',
        'title': 'Jasim Management REST API',
    },
}


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'rest_api.middleware.TelnetConnectionMiddleware'
)

ROOT_URLCONF = 'jasmin_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jasmin_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Simplify config to show/hide Swagger docs
SHOW_SWAGGER = True

'''with open(os.path.join(SETTINGS_DIR, 'local_settings.py')) as f:
    exec(f.read())'''

if SHOW_SWAGGER:
    INSTALLED_APPS += ('rest_framework_swagger',)
