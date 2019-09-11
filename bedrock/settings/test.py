from bedrock.settings import *  # noqa

# this bypasses bcrypt to speed up test fixtures
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
