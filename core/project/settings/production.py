# Space check
from core.project.settings import DEBUG, ENV, SECRET_KEY  # type: ignore

# Secrete key
SECRET_KEY = SECRET_KEY

# Allowed Host
ALLOWED_HOSTS = ENV.config('ALLOWED_HOSTS', cast=ENV.Csv())

# Debug
DEBUG = DEBUG

# Database
DATABASES = {
    'default': {
        'ENGINE': ENV.config('ENGINE'),
        'NAME': ENV.config('NAME'),
        'HOST': ENV.config('HOST'),
        'USER': ENV.config('USER'),
        'PASSWORD': ENV.config('PASSWORD'),
        'PORT': ENV.config('PORT'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Cors
CORS_ORIGIN_ALLOW_ALL = True

# Security Settings In Production Environment
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 15768000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
# Prefix session cookie with '__Host-'
SESSION_COOKIE_NAME = '__Host-sessionid'
# Prefix CSRF cookie with '__Host-'
CSRF_COOKIE_NAME = '__Host-csrftoken'

# Cors settings
CORS_ALLOWED_ORIGINS = ['https://spotterdjangoproject.com']
