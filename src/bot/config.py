from functools import cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

from bot.internal.helpers import assign_config_dict
from bot.enums import Stage


class BotConfig(BaseSettings):
    admin: int
    token: SecretStr
    stage: Stage

    model_config = assign_config_dict(prefix="BOT_")


class RedisConfig(BaseSettings):
    host: str
    port: int
    username: str
    password: SecretStr

    model_config = assign_config_dict(prefix="REDIS_")


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
            f"postgresql+asyncpg://" f"{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"
        )

    model_config = assign_config_dict(prefix="DB_")


class Settings(BaseSettings):
    bot: BotConfig = Field(default_factory=BotConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    db: DBConfig = Field(default_factory=DBConfig)

    model_config = assign_config_dict()


@cache
def get_settings() -> Settings:
    return Settings()
