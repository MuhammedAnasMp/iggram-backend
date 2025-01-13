
from firebase_admin import credentials
import firebase_admin
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-qrx0xn=$q-odldswv!7sr&c*7cl)zkmefx!7yi69w5t(+rxl^v'


cred = credentials.Certificate({
    "type": os.environ.get('FIREBASE_TYPE'),
    "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
    "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.environ.get('FIREBASE_PRIVATE_KEY').replace("\\n", "\n"),
    "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
    "auth_uri": os.environ.get('FIREBASE_AUTH_URI'),
    "token_uri": os.environ.get('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.environ.get('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_X509_CERT_URL')
})

firebase_admin.initialize_app(cred)


AUTH_USER_MODEL = 'authentication.UserProfile'

CLOUDINARY = {
    'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.getenv('CLOUDINARY_API_KEY'),
    'api_secret': os.getenv('CLOUDINARY_API_SECRET'),
}

DEBUG = os.getenv('DEBUG', 'False') == 'True'
if DEBUG:
    ALLOWED_HOSTS = ['*']
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",  # React development server
    ]
    CSRF_TRUSTED_ORIGINS = [
        'http://localhost:5173',
        'http://127.0.0.1:5173',  # Another local development URL if needed
    ]
else:
    ALLOWED_HOSTS = [
        os.getenv('BACKEND_HOST', '')
    ]
    CORS_ALLOWED_ORIGINS = [
        os.getenv('FRONTEND_DOMAIN', ''),  # Add production domain
    ]
    CSRF_TRUSTED_ORIGINS = [
        os.getenv('FRONTEND_DOMAIN', '')
    ]
CORS_ALLOW_CREDENTIALS = True
# Application definition
print('ALLOWED_HOSTS', ALLOWED_HOSTS)
print('CORS_ALLOWED_ORIGINS', CORS_ALLOWED_ORIGINS)
print('CSRF_TRUSTED_ORIGINS', CSRF_TRUSTED_ORIGINS)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.authentication',
    'rest_framework',
    'corsheaders',
    'cloudinary',
    'cloudinary_storage',

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
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT support
        'rest_framework.authentication.SessionAuthentication',         # Session support
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # Default: Require authentication
        'rest_framework.permissions.IsAuthenticated',
    ],
}


ROOT_URLCONF = 'iggrambackend.urls'

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

WSGI_APPLICATION = 'iggrambackend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True


CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_HTTPONLY = False  # Must be False to allow JavaScript to read the cookie
CSRF_COOKIE_SAMESITE = 'Lax'  # Adjust as necessary; 'None' requires HTTPS
CSRF_COOKIE_SECURE = True
