import logging
import sys
from typing import Any, Dict, List, Tuple, Type

from loguru import logger
from pydantic import SecretStr

from functools import lru_cache

from src.logging import InterceptHandler
from src.settings.base import *


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI Notes Application"
    version: str = "1.0"

    max_connection_count: int = 10
    min_connection_count: int = 10

    secret_key: SecretStr = "d04b9d7a34f0ccf23b5e0c511383e6ff645bb4632a1a1ff7440f2d386f3f21cf"

    api_prefix: str = "/api"

    jwt_token_prefix: str = "Bearer"

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [
                InterceptHandler(level=self.logging_level)]

        logger.configure(
            handlers=[{"sink": sys.stderr, "level": self.logging_level}])


from src.settings.development import DevAppSettings
from src.settings.production import ProdAppSettings
from src.settings.test import TestAppSettings

environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
}


@lru_cache
def get_app_settings():
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
