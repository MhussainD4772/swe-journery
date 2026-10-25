from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

_ENV_FILE = Path(__file__).resolve().parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Option 1 (local / compose): one full connection string
    database_url: str | None = None

    # Option 2 (AWS): separate parts; DB_PASSWORD comes from the RDS secret
    db_host: str | None = None
    db_port: int = 5432
    db_name: str | None = None
    db_user: str | None = None
    db_password: str | None = None

    @model_validator(mode="after")
    def build_database_url(self):
        # If a full URL was given, use it as-is
        if self.database_url:
            return self
        # Otherwise all four parts are required
        if not all([self.db_host, self.db_name, self.db_user, self.db_password]):
            raise ValueError(
                "Set DATABASE_URL, or DB_HOST, DB_NAME, DB_USER and DB_PASSWORD"
            )
        # URL.create safely escapes special characters in the generated password
        self.database_url = URL.create(
            "postgresql+psycopg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        ).render_as_string(hide_password=False)
        return self


settings = Settings()