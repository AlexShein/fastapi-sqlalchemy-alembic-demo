from pydantic_settings import BaseSettings


class Environment(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5438
    DB_NAME: str = "fsa-demo-db"
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"


env = Environment()
