from app.core.settings.base import AppSettings


class ProdSettings(AppSettings):
    class Config(AppSettings.Config):
        env_file = "prod.env"
