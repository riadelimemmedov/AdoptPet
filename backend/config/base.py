import mimetypes
import os
from pathlib import Path

from decouple import config
from django.utils.translation import gettext_lazy as _

# !Your everywhere service name
SITE_NAME = ""  # Domain Name

# !Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# !App Name
APP_NAME = "ADMIN"  # Default ADMIN,BOOK

# !SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-97(!!1=_(2xgj%)pp2&6bn8x@0^g6b1ps5ea24*i2tnc-!3%tq",
)


# !# PROD, LOCAL, DEV
ENVIRONMENT = config("ENVIRONMENT", default="LOCAL")
# In order to allow access to the Django app from any server or IP
# address,ensure ALLOWED_HOSTS in settings.py file set to *,as shown in
# the left
ALLOWED_HOSTS = []

if ENVIRONMENT != "LOCAL":
    pass
else:
    ALLOWED_HOSTS.append("*")


# !Application definition
DEFAULT_APPS = [
    "jet.dashboard",
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# !Third Part App
THIRD_PARTY_APPS = [
    "django_cleanup",
    "django_extensions",
    "rest_framework",
    "drf_spectacular",
    "djmoney",
    "colorfield",
    "storages",
    "debug_toolbar",
]

# !Created Apps
CREATED_APPS = ["apps.users", "apps.user_profile", "apps.pet", "apps.upload"]

# !Installed Apps
INSTALLED_APPS = DEFAULT_APPS + CREATED_APPS + THIRD_PARTY_APPS


# !AUTH_USER_MODEL
AUTH_USER_MODEL = "users.CustomUser"


# !Middleware
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "apps.account.middleware.RedirectAuthenticatedMiddleware",
    "middleware.metric.metric_middleware",
]

# !Root UrlConf
ROOT_URLCONF = "config.urls"

# !Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# !Wsgi Application
WSGI_APPLICATION = "config.wsgi.application"


# !AUTH USER MODEL
# AUTH_USER_MODEL = 'account.Account'

# !Auth Password Validators
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
#     },
# ]

# !Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en"  # production => az

LANGUAGES = [
    ("az", _("Azerbaijani")),
    ("en", _("English")),
    ("ru", _("Russian")),
]
TIME_ZONE = "Asia/Baku"
USE_I18N = True  # A boolean that specifies whether Django's translation system should be enabled
# USE_L10N = True #Numbers and dates using the format of the current locale.
USE_TZ = True  # A boolean indicating whether time zones are used in the application.


# !DATE_INPUT_FORMATS
# DATE_INPUT_FORMATS = ['%m-%d-%Y']


# !Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "static/"


# !Default Auto Field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# !Static Files
ENVIRONMENT = config("ENVIRONMENT")
if ENVIRONMENT == "LOCAL" or ENVIRONMENT == "PROD":
    # STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
# else:#if site deployed to production
#     STATIC_ROOT = os.path.join(BASE_DIR,'static')#for production


# !Django Debug Toolbar
if ENVIRONMENT == "LOCAL":
    INTERNAL_IPS = [
        "127.0.0.1",
    ]


# !MediuUrl and MediaRoot
# MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# !Jet Themes
JET_THEMES = [
    {
        "theme": "default",  # theme folder name
        "color": "#47bac1",  # color of the theme's button in user menu
        "title": "Default",  # theme title
    },
    {"theme": "violet", "color": "#a464c4", "title": "Violet"},
    {"theme": "green", "color": "#44b78b", "title": "Green"},
    {"theme": "light-green", "color": "#2faa60", "title": "Light Green"},
    {"theme": "light-violet", "color": "#a464c4", "title": "Light Violet"},
    {"theme": "light-blue", "color": "#5EADDE", "title": "Light Blue"},
    {"theme": "light-gray", "color": "#222", "title": "Light Gray"},
]


# !Celery

# Localhost
# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = "redis://localhost:6379"

# Docker
# CELERY_BROKER_URL = config(
#     "CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672/"
# )  # Second 'redis' keyword refer container name of redis
# CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", "redis://redis:6379")


# !Django Celery Results Configuration
# CELERY_RESULT_BACKEND = "django-db"  # => django_celery_results

# !Django Celery Beat Configuration
# CELERY_BEAT_SCHEDULER = (
#     "django_celery_beat.schedulers.DatabaseScheduler"  # => django_celery_beat
# )


# !Email Configuration
# EMAIL_BACKEND = config("EMAIL_BACKEND")
# EMAIL_HOST = config("EMAIL_HOST")
# EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
# EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
# EMAIL_HOST_USER = config("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
# DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")


# !Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# !SPECTACULAR_SETTINGS
SPECTACULAR_SETTINGS = {
    "TITLE": "Django DRF Ecommerce",
    "DESCRIPTION": "This project purpose creating ecommerce api for business company",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# !S3 Storage
USE_S3 = config("USE_S3", cast=bool)
if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = None
    AWS_S3_ENDPOINT_URL = config("AWS_S3_ENDPOINT_URL")
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = "media"
    MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}media/"
    DEFAULT_FILE_STORAGE = "config.storage_backends.PublicMediaStorage"
    # s3 private media settings
    PRIVATE_MEDIA_LOCATION = "private"
    PRIVATE_FILE_STORAGE = "config.storage_backends.PrivateMediaStorage"
else:
    MEDIA_URL = "/mediafiles/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")


# !FORMS_URLFIELD_ASSUME_HTTPS
FORMS_URLFIELD_ASSUME_HTTPS = True


# !Configure mimetypes
mimetypes.add_type("application/javascript", ".js", True)

# !Settings up Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}
