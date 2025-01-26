# here for reference while developing file IO
from typing import Dict, Any
import json

class KeybindConfig:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config if config else {}

    @property
    def binds(self) -> Dict[str, str]:
        return self.config.get('binds')

    @property
    def settings(self) -> Dict[str, Any]:
        return self.config.get('settings')

    def __getitem__(self, key: str) -> Any:
        return self.config.get(key)

    def __setitem__(self, key: str, value: Any):
        self.config[key] = value

    def __repr__(self) -> str:
        return f'KeybindConfig({self.config})'

    def __str__(self) -> str:
        return str(self.config)

    def filter_bindings(self, kid: str) -> Dict[str, str]:
        fkeys = filter(lambda combo: combo.startswith(kid), self.binds)
        return {k: self.binds.get(k) for k in fkeys}

    def get_setting(self, key: str) -> Any:
        if key in self.config:
            return self.config[key]
        elif key in self.binds:
            return self.binds[key]
        elif key in self.settings:
            return self.settings[key]
        else:
            raise KeyError(f'Setting {key} not found')

    def _set_setting_(self, key: str, value: Any):
        """
        bypasses type checking. Do not use. ever.
        I wrote it and have no idea what I'm doing. Use multiprocessing or threads and
        everything will catch fire. A race condition will always occur corrupting all open file handles.
        There is no failback or recovery method and definitely no error correction.
        """
        self.config[key] = value

    def update_setting(self, key: str, value: Any):
        if key in self.config:
            if isinstance(self.config[key], type(value)):
                self.config[key] = value
            else:
                self.config[key]

        elif key in self.binds:
            if isinstance(self.binds[key], type(value)):
                self.binds[key] = value
            else:
                self.binds[key]

        elif key in self.settings:
            if isinstance(self.settings[key], type(value)):
                self.settings[key] = value
            else:
                self.settings[key]

        else:
            raise KeyError(f'Setting {key} not found')

    def get_keybinds(self) -> Dict[str, str]:
        return self.binds

conFile = 'form_data.json'
conDict = json.load(open(conFile, 'rb'))

hotKeys = conDict['binds']
settings = conDict['settings']

all_binds = KeybindConfig({'binds': hotKeys, 'settings': settings})

binds_no_cap = all_binds.filter_bindings('ctrl')
config_no_cap = all_binds.settings.copy()

no_cap = KeybindConfig({'binds': binds_no_cap, 'settings': config_no_cap})
no_cap.update_setting('capitalize', False)

if __name__ == '__main__':
    print(f'All binds: {all_binds}')
    print(f'No caps: {no_cap}')
