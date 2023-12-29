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
    _postgres_db_engine = env.str("POSTGRES_DB_ENGINE")
    _postgres_db_name = env.str("POSTGRES_DB_NAME")
    _postgres_user = env.str("POSTGRES_USER")
    _postgres_password = env.str("POSTGRES_PASSWORD")
    _postgres_host = env.str("POSTGRES_HOST")
    _allowed_hosts = env.list("ALLOWED_HOSTS")
    _celery_broker_url = env.str("CELERY_BROKER_URL")
    _celery_result_backend = env.str("CELERY_RESULT_BACKEND")
    _celery_accept_content = env.list("CELERY_ACCEPT_CONTENT")
    _celery_task_serializer = env.str("CELERY_TASK_SERIALIZER")
    _celery_result_serializer = env.str("CELERY_RESULT_SERIALIZER")
    _celery_ignore_result = env.str("CELERY_IGNORE_RESULT")
    _celery_track_started = env.str("CELERY_TRACK_STARTED")
    #_selenium_container_name = env.str("SELENIUM_CONTAINTER_NAME")

    
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
    def get_postgres_db_engine(cls) -> str:
        if cls._postgres_db_engine is None:
            raise ValueError("Postgres database engine is not provided.")
        return cls._postgres_db_engine

    @classmethod
    def get_postgres_db_name(cls) -> str:
        if cls._postgres_db_name is None:
            raise ValueError("Postgres database name is not provided.")
        return cls._postgres_db_name

    @classmethod
    def get_postgres_user(cls) -> str:
        if cls._postgres_user is None:
            raise ValueError("Postgres user is not provided.")
        return cls._postgres_user

    @classmethod
    def get_postgres_password(cls) -> str:
        if cls._postgres_password is None:
            raise ValueError("Postgres password is not provided.")
        return cls._postgres_password

    @classmethod
    def get_postgres_host(cls) -> list:
        if cls._postgres_host is None:
            raise ValueError("Postgres host is not provided.")
        return cls._postgres_host

    @classmethod
    def get_allowed_hosts(cls) -> str:
        if cls._allowed_hosts is None:
            raise ValueError("Allowed hosts are not provided.")
        return cls._allowed_hosts

    @classmethod
    def get_celery_broker_url(cls) -> str:
        if cls._celery_broker_url is None:
            raise ValueError("Celery broker url is not provided.")
        return cls._celery_broker_url

    @classmethod
    def get_celery_result_backend(cls) -> str:
        if cls._celery_result_backend is None:
            raise ValueError("Celery result backend is not provided.")
        return cls._celery_result_backend

    @classmethod
    def get_celery_accept_content(cls) -> list:
        if cls._celery_accept_content is None:
            raise ValueError("Celery accept content is not provided.")
        return cls._celery_accept_content

    @classmethod
    def get_celery_task_serializer(cls) -> str:
        if cls._celery_task_serializer is None:
            raise ValueError("Celery task serializer is not provided.")
        return cls._celery_task_serializer

    @classmethod
    def get_celery_result_serializer(cls) -> str:
        if cls._celery_result_serializer is None:
            raise ValueError("Celery result serializer is not provided.")
        return cls._celery_result_serializer

    @classmethod
    def get_celery_ignore_result(cls) -> bool:
        if cls._celery_ignore_result is None:
            raise ValueError("Celery ignore result is not provided.")
        return cls._celery_ignore_result

    @classmethod
    def get_celery_track_started(cls) -> bool:
        if cls._celery_track_started is None:
            raise ValueError("Celery track started is not provided.")
        return cls._celery_track_started
    
    '''@classmethod
    def get_selenium_container_name(cls) -> str:
        if cls._selenium_container_name is None:
            raise ValueError("Selenium container name is not provided.")
        return cls._selenium_container_name'''