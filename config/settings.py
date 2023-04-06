import datetime
import os
from pathlib import Path
from decouple import Config, RepositoryEnv, config
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# CORE SETTINGS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_ENV = os.environ.get('SERVER_ENV', 'dev')
if SERVER_ENV == 'dev':
    ENV_FILE = os.path.join(BASE_DIR, '.env.example')
    env_config = Config(RepositoryEnv(ENV_FILE))
else:
    env_config = config

SECRET_KEY = env_config('SECRET_KEY')
DEBUG = env_config("DEBUG", cast=bool)
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.user',
    'apps.authentication',

    'drf_yasg',
    'corsheaders',
    'rest_framework',
    'django_celery_beat',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'apps.core.middleware.CurrentUserMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

SILK_ENABLE = env_config("SILK_ENABLE", cast=bool)
if SILK_ENABLE:
    INSTALLED_APPS += [
        'silk',
    ]
    MIDDLEWARE += [
        'silk.middleware.SilkyMiddleware',
    ]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
AUTH_USER_MODEL = 'user.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# CORS SETTINGS
CORS_ALLOWED_ORIGINS = [
    'http://localhost',
]

# TEMPLATES SETTINGS
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# DATABASE SETTINGS
if env_config('DATABASES_NAME', 'None').lower() == 'postgres':
    DATABASES = {
        "default": {
            "ENGINE": env_config("POSTGRES_ENGINE", "django.db.backends.sqlite3"),
            "NAME": env_config("POSTGRES_DB", os.path.join(BASE_DIR, "db.sqlite3")),
            "USER": env_config("POSTGRES_USER", "admin"),
            "PASSWORD": env_config("POSTGRES_PASSWORD", "admin"),
            "HOST": env_config("POSTGRES_HOST", "localhost"),
            "PORT": env_config("POSTGRES_PORT", "5432"),
        }
    }
elif env_config('DATABASES_NAME', 'None').lower() == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': env_config("MY_SQL_ENGINE", "django.db.backends.sqlite3"),
            'NAME': env_config("MYSQL_DATABASE", "db"),
            'USER': env_config("MYSQL_USER", "admin"),
            'PASSWORD': env_config("MYSQL_PASSWORD", "admin"),
            'HOST': env_config("MY_SQL_HOST", "127.0.0.1"),
            'PORT': env_config("MYSQL_PORT", "3306"),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

# AUTH_PASSWORD_VALIDATORS
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# I18N SETTINGS
LANGUAGE_CODE = env_config('LANGUAGE_CODE')
TIME_ZONE = env_config('TIME_ZONE')
USE_I18N = True
USE_L10N = False
USE_TZ = True

# STATIC FILES SETTINGS
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# REST_FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER':
        'apps.core.exception_handler.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '60/min',
    }
}

# SWAGGER_SETTINGS
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        "Token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        },
    },
}

# JWT SETTINGS
JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': 'JWT',
}

# LOGGING SETTINGS
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d}: {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
    }
}

# AUTHENTICATION BACKENDS SETTINGS
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'apps.core.authentication_backend.SettingsBackend',
]

# EMAIL SETTINGS
EMAIL_HOST = env_config('EMAIL_HOST')
EMAIL_BACKEND = env_config('EMAIL_BACKEND')
EMAIL_PORT = env_config('EMAIL_PORT')
EMAIL_HOST_USER = env_config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env_config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env_config('EMAIL_USE_TLS', cast=bool)
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# MESSAGE QUEUE SETTINGS
CELERY_BROKER_URL = env_config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env_config('CELERY_BROKER_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# CACHES SETTINGS
if env_config('CACHE_DRIVER') == 'redis':
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env_config('CACHES_URL'),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient"
            }
        }
    }

# SECURITY SETTINGS
if SERVER_ENV != 'dev':
    SECURE_HSTS_SECONDS = 1
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
    CSRF_COOKIE_SECURE = True


if os.environ.get('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
    )
