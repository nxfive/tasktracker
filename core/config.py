from functools import lru_cache
from core.settings.base import AppSettings, BaseAppSettings, EnvState
from core.settings.dev import DevSettings
from core.settings.prod import ProdSettings
from core.settings.test import TestSettings
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
