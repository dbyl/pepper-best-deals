import os

import environ


class CustomEnvironment:
    env = environ.Env()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

    _debug = env.str("DEBUG")
    _secret_key = env.str("SECRET_KEY")
    _url = env.str("URL")
    _database_url = env.str("DATABASE_URL")
    _allowed_hosts = env.str("ALLOWED_HOSTS")
    _email = env.str("EMAIL")
    _email_password = env.str("EMAIL_PASSWORD")

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

    @classmethod
    def get_email(cls) -> str:
        if cls._email is None:
            raise ValueError("Email is not provided.")
        return cls._email

    @classmethod
    def get_email_password(cls) -> str:
        if cls._email_password is None:
            raise ValueError("Email password is not provided.")
        return cls._email_password