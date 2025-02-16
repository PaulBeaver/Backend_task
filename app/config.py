import sys

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.

    Attributes:
        DB_PORT (str): Database port.
        DB_NAME (str): Database name.
        DB_USER (str): Database username.
        DB_PASS (str): Database password.
        DB_HOST (str): Database host address.
    """

    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str

    @property
    def DATABASE_URL(self) -> str:
        """
        Builds the database connection URL using the provided settings.

        Returns:
            str: The PostgreSQL database connection URL for asyncpg.
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        """
        Pydantic configuration class for environment file loading.

        Chooses between ".env-tests" and ".env" depending on test execution.
        """

        env_file = ".env-tests" if "pytest" in sys.modules else ".env"
        env_file_encoding = "utf-8"


# Instantiate settings object that will be imported and used across the application.
settings = Settings()
