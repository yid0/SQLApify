def get_env(key: str):
    from os import getenv

    return getenv(str(key))
