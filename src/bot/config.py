from functools import cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

from bot.internal.enums import Stage
from bot.internal.helpers import assign_config_dict


class BotConfig(BaseSettings):
    admin: int
    token: SecretStr
    stage: Stage
    geoname: str
    geostring: SecretStr

    model_config = assign_config_dict(prefix="BOT_")


class DBConfig(BaseSettings):
    user: str
    password: SecretStr
    host: str
    port: int
    name: str
    echo: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    @property
    def pg_dsn(self) -> SecretStr:
        return SecretStr(
            f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"
        )

    model_config = assign_config_dict(prefix="DB_")


class Settings(BaseSettings):
    bot: BotConfig = Field(default_factory=BotConfig)
    db: DBConfig = Field(default_factory=DBConfig)

    model_config = assign_config_dict()


@cache
def get_settings() -> Settings:
    return Settings()
