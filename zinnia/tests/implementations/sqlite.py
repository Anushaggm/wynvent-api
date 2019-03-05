"""Settings for testing zinnia on SQLite"""

DATABASES = {
    'default': {
        'NAME': 'zinnia.db',
        'ENGINE': 'django.db.backends.sqlite3'
    }
}
