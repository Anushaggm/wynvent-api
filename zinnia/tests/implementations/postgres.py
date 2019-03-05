"""Settings for testing zinnia on Postgres"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'zinnia',
        'USER': 'postgres',
        'HOST': 'localhost'
    }
}
