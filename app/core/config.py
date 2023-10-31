from functools import lru_cache
from app.core.settings.base import AppSettings, BaseAppSettings, EnvState
from app.core.settings.dev import DevSettings
from app.core.settings.prod import ProdSettings
from app.core.settings.test import TestSettings
from typing import Dict, Type

settings_mapping: Dict[EnvState, Type[AppSettings]] = {
    EnvState.dev: DevSettings,
    EnvState.prod: ProdSettings,
    EnvState.test: TestSettings,
}


@lru_cache()
def get_settings() -> AppSettings:
    env_state = BaseAppSettings().env_state
    print(env_state)
    return settings_mapping[env_state]()
