#Create an .env file in your project dir.

#These are the ENV VARS that needs to be set:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = '.....@gmail.com'

EMAIL_HOST_PASSWORD = 'password'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SECRET_KEY = "secret_code"

DEBUG = True

MOBILE_HOST_USER = '+5999-'

FACEBOOK_USER="https://www.facebook.com/username"

LINKEDIN_USER="https://www.linkedin.com/in/username/"

INSTAGRAM_USER=""