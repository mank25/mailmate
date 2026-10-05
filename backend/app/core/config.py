from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str
    token_encryption_key: str
    frontend_url: str = "http://localhost:3000"
    # Set false when serving over plain http on a non-localhost address (e.g. a LAN IP)
    cookie_secure: bool = True
    # The first account can always sign up; additional signups need this enabled
    allow_signup: bool = False

    @model_validator(mode="after")
    def _reject_placeholder_secrets(self):
        for name in ("secret_key", "token_encryption_key"):
            if "CHANGE_ME" in getattr(self, name):
                raise ValueError(f"{name.upper()} is still the placeholder; set a real value in .env")
        return self

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
