import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'c9',
        'USER': os.getenv('C9_USER'),
        'HOST': os.getenv('IP'),
    }
}
