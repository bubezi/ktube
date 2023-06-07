from pathlib import Path
import os
import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = ['ktube.pythonanywhere.com']
ALLOWED_HOSTS += ['192.168.87.137', '127.0.0.1']



######################## COMMENT THIS OUT DURING DEVELOPMENT AND TESTING AND UNCOMMENT THE ONE BELOW IT ###########################################

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False

# # Database
# # https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': env("DB_NAME"),
#         'USER': env("DB_USER"),
#         'PASSWORD': env("DB_PASSWORD"),
#         'HOST': env("DB_HOST"),
#     }
# }


#########################################################################################################################################################






######################## COMMENT THIS OUT WHEN DEPLOYING TO PRODUCTION AND UNCOMMENT THE ONE ABOVE IT ###############################################



DEBUG = True


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': env("DB_NAME_DEV"),
#         'USER': env("DB_USER_DEV"),
#         'PASSWORD': env("DB_PASSWORD_DEV"),
#         'HOST': env("DB_HOST_DEV"),
#         'PORT': env("DB_PORT_DEV"),
#     }
# }


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


#########################################################################################################################################################






# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
    
    # Own Apps
    'tube',
    'register',    
    
    # Third-party apps
    'django.contrib.humanize',
    'django_filters',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_cleanup.apps.CleanupConfig',
]



# SITE_ID = 1
## ###########UPDATE site.domain in python manage.py shell after Hosting/production
## #Or set it to id=2 ### Site.objects.get(id=2)
## #COMMANDS
## #python manage.py shell
## >from django.contrib.sites.models import Site
## >site = Site.objects.get(id=2)
## >site.domain = 'my_domain.com'
## >site.save()
## ### Then set SITE_ID = 2

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ktube.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'ktube.wsgi.application'





# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
   ]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Base url to serve media files
MEDIA_URL = '/media/'

# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/bye"


##############################################################################################
#############################                                   ##############################
#############################                                   ##############################
#############################           DEPLOY SETTINGS         ##############################
#############################                                   ##############################
#############################                                   ##############################
##############################################################################################


# # Email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = env("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

# # Stripe settings
# STRIPE_PUBLISHABLE_KEY = env("STRIPE_PUBLISHABLE_KEY")


# # HTTPS settings
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# # # HSTS settings
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# # # X-Frame-Options
# SECURE_FRAME_DENY = True

# # # X-Content-Type-Options
# SECURE_CONTENT_TYPE_NOSNIFF = True

# # # X-XSS-Protection
# SECURE_BROWSER_XSS_FILTER = True

# # # Referrer-Policy
# REFERRER_POLICY = 'same-origin'

# # # Content-Security-Policy
# # # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
# CSP_DEFAULT_SRC = ("'self'",)
# CSP_SCRIPT_SRC = ("'self'",)
# CSP_STYLE_SRC = ("'self'",)
# CSP_IMG_SRC = ("'self'",)
# CSP_FONT_SRC = ("'self'",)
# CSP_CONNECT_SRC = ("'self'",)
# CSP_BASE_URI = ("'self'",)
# CSP_FORM_ACTION = ("'self'",)
# CSP_FRAME_ANCESTORS = ("'self'",)
# CSP_OBJECT_SRC = ("'none'",)
# CSP_MEDIA_SRC = ("'none'",)
# CSP_WORKER_SRC = ("'none'",)
# CSP_FRAME_SRC = ("'none'",)
# CSP_SANDBOX = ("allow-forms", "allow-scripts", "allow-same-origin")
# CSP_REPORT_URI = "/csp-report/"


# # # X-Permitted-Cross-Domain-Policies
# X_PERMITTED_CROSS_DOMAIN_POLICIES = 'none'

# # # X-Download-Options
# X_DOWNLOAD_OPTIONS = 'noopen'

# # # X-Content-Type-Options
# X_CONTENT_TYPE_OPTIONS = 'nosniff'

# # # X-Frame-Options
# X_FRAME_OPTIONS = 'DENY'

# # # X-XSS-Protection
# X_XSS_PROTECTION = '1; mode=block'

# # # Referrer-Policy
# REFERRER_POLICY = 'same-origin'

