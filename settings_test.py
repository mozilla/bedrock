# These settings will always be overriding for all test runs

# this bypasses bcrypt to speed up test fixtures
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
