#!/usr/bin/python3
# class to handle hotkeys key combos are: ctrl+shift+<key>
import subprocess
import importlib
import pickle
import keyboard
import mouse
import german_ahk as ghk
from hkWarnings import notImplementedWarning
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def save_obj(obj, name):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, -1)
        
def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)
    
class ConfigChangeHandler(FileSystemEventHandler):
    def __init__(self, hk_manager):
        self.hk_manager = hk_manager

    def on_modified(self, event):
        if event.src_path.endswith('form_data.json'):
            print(f'form_data.json has been modified. Reloading config...')
            self.hk_manager.reload_config()

class hkManager:
    def __init__(self,fname='keyBindReg.pkl') -> None:
        """
        summary: Object to manage hotkeys and bind them to functions.
        Hotkey callbacks are generics and call the write method with the target string.
        This example is for german characters on a US keyboard layout. 
        Capitalization is supported by replacing ctrl modifier with shift.
    
        """
        self.fname = fname
        self.config = ghk.all_binds
        self.key_binds = self.config.binds
        self.cap_binds = self.config.settings['capitalize']
        self.warning = False
        self.menuVisible = False
        
    def __str__(self) -> str:
        # return a string representation of the key_binds dict
        return str(self.config)
    
    def start_watching(self):
        event_handler = ConfigChangeHandler(self)
        observer = Observer()
        observer.schedule(event_handler, path='.', recursive=False)
        observer.start()
        return observer
    
    def getBinds(self,exclude:list=[]):
        """returns a list of the keyBinds dict keys

        Args:
            exclude (list, optional): list of keys to exclude from the list. Defaults to [].

        Returns:
            list: list of keyBinds dict keys
        """
        return [key for key in self.key_binds.keys() if key not in exclude]
    
    def add_hotkey(self, keys:str, func):
        """adds a hotkey to the keyboard and mouse hooks"""
        keyboard.add_hotkey(keys, func)
       
    def add_hotkeys(self, hotkeys:list):
        """adds hotkeys to the keyboard and mouse hooks

        Args:
            hotkeys (list): list of strings that are either:
                'key combos'|'mouse events' to hook.
        """
        for key in hotkeys:
            target = self.key_binds[key]
            keyboard.add_hotkey(key, self.write, args=[str(target)])
            # add a version with caps for the hotkey if the setting is enabled
            if self.cap_binds:
                self.add_caps_hotkey(key, target)

    def add_caps_hotkey(self, key, target):
        k_seq:list = key.split('+')
        k_seq.remove('ctrl')
        k_seq.insert(0, 'shift')
        cap_hk = '+'.join(k_seq)
        self.key_binds[cap_hk] = target.upper()
        keyboard.add_hotkey(cap_hk, self.write, args=[str(target.upper())])
        
    def show_config(self):
        # launch the form with the keybinds
        if not self.menuVisible:
            try:
                self.menu = subprocess.Popen(['python', 
                                            'form_generator.py',
                                            str(self.config)], 
                                            )
                self.menuVisible = True
            except notImplementedWarning as e:
                print(e.message)
            except Exception as e:
                print(e)
                print('Failed to launch the config menu')
        else:
            try:
                self.menu.kill()
                self.menuVisible = False
            except Exception as e:
                print(e)
                print('Failed to close the config menu')
        
    def remove_hotkeys(self, hotkeys:list):
        """removes hotkeys from the keyboard and mouse hooks

        Args:
            hotkeys (list): list of strings that are either:
                'key combos'|'mouse events' to unhook.
        """   
        for key in hotkeys:
            if key in self.key_binds:
                keyboard.remove_hotkey(key)
    
    def kill_all(self):
        """unhooks all hotkeys from the keyboard and mouse hooks"""
        keyboard.unhook_all()
        mouse.unhook_all()
   
    def wait(self, keysDown:str):
        return keyboard.wait(keysDown)

    def write(self, text:str):
        # 
        print(f'writing: {text}')
        return keyboard.write(text)
    
    def reload_config(self):
        # reload the german_ahk module
        importlib.reload(ghk)
        self.config = ghk.all_binds
        self.key_binds = self.config.binds
        self.cap_binds = self.config.settings['capitalize']
        print('Config reloaded')
        # update the hotkeys
        self.remove_hotkeys(self.key_binds.keys())
        self.add_hotkeys(self.getBinds(exclude=['ctrl+win', 'win+ctrl']))
        
def main():
    prevState = load_obj('keyBindReg_german.pkl')
    t = hkManager(fname='keyBindReg_german.pkl')
    # start the listener
    print('Hotkeys are active')
    # static hotkeys are added here, dynamic hotkeys are added in the config menu
    # adding static hotkeys anywhere else sets everything on fire.
    t.add_hotkey('win+ctrl', t.show_config)
    # t.add_hotkey('alt+shift+r', t.reload_config)
    t.add_hotkeys(t.getBinds(exclude=['ctrl+win']))

    # Start watching for config changes
    observer = t.start_watching()

    try:
        # wait here or the program will become recursive on reload with no way to exit.
        t.wait('ctrl+shift+q')
    finally:
        observer.stop()
        observer.join()
        # MAKE SURE POPEN IS NEVER SET TO 'shell=True'
        # 'shell=True' leaves an orphaned process because the shell becomes a child process and closes before the menu sees SIGKILL
        try:
            t.menu.kill()
        except Exception as e:
            print(e)    
        # unhook all hotkeys and listeners
        t.kill_all()
        # save the config state to a file to keep fail back state on next run.
        save_obj(t.config, t.fname)
        print(t)
    
if __name__ == "__main__":
    main()