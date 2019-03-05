"""Settings for testing zinnia on MySQL"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zinnia',
        'USER': 'root',
        'HOST': 'localhost'
    }
}
