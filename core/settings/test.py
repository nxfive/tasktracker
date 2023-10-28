from core.settings.base import AppSettings


class TestSettings(AppSettings):
    debug: bool = True

    class Config(AppSettings.Config):
        env_file = ".env"
        env_prefix = "TEST_"
