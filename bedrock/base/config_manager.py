from everett.manager import (
    ConfigEnvFileEnv,
    ConfigManager,
    ConfigOSEnv,
)


config = ConfigManager([
    # first check for environment variables
    ConfigOSEnv(),
    # then look in the .env file
    ConfigEnvFileEnv('.env'),
])
