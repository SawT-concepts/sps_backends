import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y2h4j0z$c7mm0^5p4wj873e7-ne02ur^s+wihopj^^$4v4h(dg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True


CORS_ALLOW_HEADERS = ['*']


INSTALLED_APPS = [
    "corsheaders",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',

    # Installed_apps
    'Api',
    's_admin',
    'Configuration',
    'Payments',
    'Dashboard',
    "crispy_forms",
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'django_filters',
    'rest_framework',

]


SITE_ID = 1

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'sps_backends.urls'

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
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            }
        },
    },
]


WSGI_APPLICATION = 'sps_backends.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CSRF_TRUSTED_ORIGINS = ['https://myspsonline.com',]
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# default static files settings for PythonAnywhere.
# see https://help.pythonanywhere.com/pages/DjangoStaticFiles for more info
MEDIA_ROOT = '/media'
MEDIA_URL = '/media/'
# STATIC_ROOT = BASE_DIR/"static"
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static',]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': ('rest_framework.schemas.coreapi.AutoSchema')
}


# PAYSTACK STUFFS (TAKE DOWN!!)
PAYSTACK_SECRET_KEY = "sk_test_318b13d19abb1a43caec32abaacda9d183a04ecf"
PAYSTACK_PUBLIC_KEY = "pk_test_ba7b39de2d7e2470a24a362c861a98cc479773c8"

REMITA_PUBLIC_KEY = "QzAwMDA1NTQ2NzF8MTEwMDU1MzI4MDEwfDU3MDgzMDZjNmFhY2EyNmJmYzI5N2I1YmU5YmI0ZWQ5ZWQyOGY3NmUxOTQxMWU2NDBmNjMwZGEwZGU1NDI3MDViNzBiNWVlN2I2NjZhNGEzYmY1N2U4ZDY5OTZjY2FhODI4NWMyNjI1MTIwZGE4YmZhOGQ1M2RiODJlNjUxNjQz"
REMITA_SECRET_KEY = "2352b014a8518633de2a0797b02959248ad16fd5ba08cd6196434c85c28ce4a03bcf502586a65f9a38bd24375442e3b1ce773a8db7300485c5884106327cb1c2"
# EMail stuffs
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'myspsinfo@gmail.com'
EMAIL_HOST_PASSWORD = 'rgvcsggogiebnhjh'
