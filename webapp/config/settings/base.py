"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "account.apps.AccountConfig",  # 장고가 다른 app에 정의된 템플릿 대신 이 app의 템플릿을 사용하도록 설정
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # libs
    "rest_framework",
    "django_filters",
    "social_django",
    "easy_thumbnails",
    # apps
    "images.apps.ImagesConfig",
    "actions.apps.ActionsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "account.authentication.EmailAuthBackend",
    "social_core.backends.twitter.TwitterOAuth",
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

MEDIA_URL = "media/"  # 사용자가 업로드한 미디어 파일을 제공하는 기본 URL
MEDIA_ROOT = BASE_DIR / "media"  # 미디어 파일이 있는 로컬 경로

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ]
}

# SMTP 서버 구성
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # 보낸 이메일을 console 창에 보여준다.
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "dlwhdtjd098@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", True)


# AUTH SETTINGS
LOGIN_REDIRECT_URL = (
    "dashboard"  # 요청에 next 매개 변수가 없는 경우 성공적인 로그인 후 사용자를 리디렉션할 URL을 장고에게 알려준다.
)
LOGIN_URL = "login"
LOGOUT_URL = "logout"
# X AUTH
SOCIAL_AUTH_TWITTER_KEY = os.environ.get("SOCIAL_AUTH_TWITTER_KEY")
SOCIAL_AUTH_TWITTER_SECRET = os.environ.get("SOCIAL_AUTH_TWITTER_SECRET")
# GOOGLE AUTH
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get(
    "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET"
)

# Auth PIPELINE
SOCIAL_AUTH_PIPELINE = [
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. In some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    "social_core.pipeline.social_auth.social_details",
    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    "social_core.pipeline.social_auth.social_uid",
    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    "social_core.pipeline.social_auth.auth_allowed",
    # Checks if the current social-account is already associated in the site.
    "social_core.pipeline.social_auth.social_user",
    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    "social_core.pipeline.user.get_username",
    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social_core.pipeline.mail.mail_validation',
    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    # 'social_core.pipeline.social_auth.associate_by_email',
    # Create a user account if we haven't found one yet.
    "social_core.pipeline.user.create_user",
    # Profile 생성
    "account.authentication.create_profile",
    # Create the record that associates the social account with the user.
    "social_core.pipeline.social_auth.associate_user",
    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    "social_core.pipeline.social_auth.load_extra_data",
    # Update the user record with any changed info from the auth service.
    "social_core.pipeline.user.user_details",
]


# 썸네일 디버깅 하기
# THUMBNAIL_DEBUG = True  # 디버그 정보 얻기

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda u: reverse_lazy("user_detail", args=[u.username])
}  # get_absolute_url() 메서드를 오버라이드하는 또 다른 방법


# redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
