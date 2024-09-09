"""App configuration module."""

from functools import lru_cache
from typing import Optional
from typing_extensions import Annotated, Union

import pydantic
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class GlobalConfig(BaseSettings):
    """Global configurations."""

    # This variable will be loaded from the .env file. However, if there is a
    # shell environment variable having the same name, that will take precedence.

    ENV_STATE: Annotated[
        str,
        pydantic.Field(..., validation_alias="ENV_STATE")
    ]
    # ENV_STATE: Optional[str] = pydantic.Field(None, env="ENV_STATE")  # type: ignore
    # HOST: Optional[str] = pydantic.Field(None, env="HOST")  # type: ignore
    # PORT: Optional[str] = pydantic.Field(None, env="PORT")  # type: ignore

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
        env_prefix="",
        env_nested_delimiter="_",
    )


class DevConfig(GlobalConfig):
    """Development configurations."""

    ROOT_PATH: Annotated[
        str | None,
        pydantic.Field(None, validation_alias="DEV_ROOT_PATH")
    ]
    STREAM: Annotated[
        str,
        pydantic.Field(..., validation_alias="DEV_STREAM")
    ]
    NATS_SERVER_URL: Annotated[
        str,
        pydantic.Field(..., validation_alias="DEV_NATS_SERVER_URL")
    ]
    NATS_CATASTODB_SUBJECT: Annotated[
        str,
        pydantic.Field(..., validation_alias="DEV_NATS_CATASTODB_SUBJECT")
    ]
    NATS_NOTIFICATION_SUBJECT: Annotated[
        str,
        pydantic.Field(..., validation_alias="DEV_NATS_NOTIFICATION_SUBJECT")
    ]

    model_config = SettingsConfigDict(env_prefix="DEV_")


class ProdConfig(GlobalConfig):
    """Production configurations."""

    ROOT_PATH: Annotated[
        str | None,
        pydantic.Field(None, validation_alias="PROD_ROOT_PATH")
    ]
    STREAM: Annotated[
        str,
        pydantic.Field(..., validation_alias="PROD_STREAM")
    ]
    NATS_SERVER_URL: Annotated[
        str,
        pydantic.Field(..., validation_alias="PROD_NATS_SERVER_URL")
    ]
    NATS_CATASTODB_SUBJECT: Annotated[
        str,
        pydantic.Field(..., validation_alias="PROD_NATS_CATASTODB_SUBJECT")
    ]
    NATS_NOTIFICATION_SUBJECT: Annotated[
        str,
        pydantic.Field(..., validation_alias="PROD_NATS_NOTIFICATION_SUBJECT")
    ]

    model_config = SettingsConfigDict(env_prefix="PROD_")


class FactoryConfig:
    """Returns a config instance depending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        """Initialize factory configuration."""
        self.env_state = env_state

    @lru_cache()
    def __call__(self) -> DevConfig | ProdConfig:
        """Handle runtime configuration."""
        if self.env_state == "dev":
            return DevConfig(
                **GlobalConfig(ENV_STATE=self.env_state).model_dump()
            )
        elif self.env_state == "prod":
            return ProdConfig(
                **GlobalConfig(ENV_STATE=self.env_state).model_dump()
            )
        else:
            raise ValueError


configuration = FactoryConfig(env_state=GlobalConfig().ENV_STATE)()  # type: ignore
