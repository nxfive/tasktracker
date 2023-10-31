from app.core.settings.base import AppSettings


class DevSettings(AppSettings):
    debug: bool = True

    class Config(AppSettings.Config):
        env_file = ".env"
        env_prefix = "DEV_"
