"""Configurations module."""

# conflict between isort and pylint
# pylint: disable=C0411
from functools import (
    lru_cache,
)
import os
from pathlib import (
    Path,
)
from pydantic import (
    BaseSettings,
)
from typing import (
    List,
)


class Settings(BaseSettings):
    """
    A Pydantic class that loads and stores environment variables in memory.

    Note:
        The os.getenv is used in production.

    Args:
        MONGODB_HOST (str) : MONGODB URL.
        MONGODB_USERNAME (str) : MONGODB username.
        MONGODB_PASSWORD (str) : MONGODB password.
        MONGODB_DATABASE (str) : MONGODB database name.
        JWT_SECRET_KEY (str) : A secure app jwt secret key.
        DEBUG (str) : A variable used to separate testing env from production env.
        CORS_ORIGINS (str) : A string that contains comma separated urls for cors origins.

    Example:
        >>> MONGODB_HOST=svc-123456789.svc.MONGODB.com
        >>> MONGODB_USERNAME=admin
        >>> MONGODB_PASSWORD=51R0NGPO$$W0RD
        >>> MONGODB_DATABASE=tinder
        >>> JWT_SECRET_KEY=123SDA23sa
        >>> DEBUG="" # "" means production, "test" means testing, "info" means development.
        >>> CORS_ORIGINS="https://app-name.herokuapp.com,http://app-name.pages.dev"
    """

    MONGODB_HOST: str = os.getenv("MONGODB_HOST")  # type: ignore
    MONGODB_USERNAME: str = os.getenv("MONGODB_USERNAME")  # type: ignore
    MONGODB_PASSWORD: str = os.getenv("MONGODB_PASSWORD")  # type: ignore
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE")  # type: ignore
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")  # type: ignore
    DEBUG: str = os.getenv("DEBUG")  # type: ignore
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS")  # type: ignore

    class Config:  # pylint: disable=R0903
        """
        A class used to set Pydantic configuration for env vars.
        """

        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def db_url(self) -> str:
        """
        Assemble database URL from self.

        Args:
            self ( _obj_ ) : object reference.

        Returns:
            str: The assembled database URL.
        """

        if self.DEBUG == "test":
            mongodb_database_url = (
                "mongodb+srv://"
                + self.MONGODB_USERNAME
                + ":"
                + self.MONGODB_PASSWORD
                + "@"
                + self.MONGODB_HOST
                + "/"
                + "test"
                + "?"
                + "retryWrites=true"
                + "&"
                + "w=majority"
            )

        else:
            mongodb_database_url = (
                "mongodb+srv://"
                + self.MONGODB_USERNAME
                + ":"
                + self.MONGODB_PASSWORD
                + "@"
                + self.MONGODB_HOST
                + "/"
                + self.MONGODB_DATABASE
                + "?"
                + "retryWrites=true"
                + "&"
                + "w=majority"
            )
        return mongodb_database_url

    @property
    def cors_origins(self) -> List[str]:
        """
        Build a list of urls from a comma separated values string.

        Args:
            self ( _obj_ ) : object reference.

        Returns:
            List[str]: A list of urls.
        """
        return (
            [url.strip() for url in self.CORS_ORIGINS.split(",") if url]
            if self.CORS_ORIGINS
            else []
        )


@lru_cache()
def settings() -> "Settings":
    return Settings()


# Export module

__all__ = ["settings"]
