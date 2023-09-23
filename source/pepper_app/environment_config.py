import os
from pathlib import Path

import environ


class CustomEnvironment:

    env = environ.Env(DEBUG=(bool, False))
    environ.Env.read_env()
    BASE_DIR = Path(__file__).resolve().parent.parent
    environ.Env.read_env(BASE_DIR / ".env")

    _debug = env.str("DEBUG")
    _secret_key = env("SECRET_KEY")
    _url = env.str("URL")
    _database_url = env.db("DATABASE_URL")
    _allowed_hosts = env.list("ALLOWED_HOSTS")

    @classmethod
    def get_debug(cls) -> bool:
        if cls._debug is None:
            raise ValueError("Debug is not provided.")
        return cls._debug

    @classmethod
    def get_secret_key(cls) -> str:
        if cls._secret_key is None:
            raise ValueError("Secret key is not provided.")
        return cls._secret_key

    @classmethod
    def get_url(cls) -> str:
        if cls._url is None:
            raise ValueError("Url is not provided.")
        return cls._url

    @classmethod
    def get_database_url(cls) -> str:
        if cls._database_url is None:
            raise ValueError("Database url is not provided.")
        return cls._database_url

    @classmethod
    def get_allowed_hosts(cls) -> str:
        if cls._allowed_hosts is None:
            raise ValueError("Allowed hosts are not provided.")
        return cls._allowed_hosts
