#!/usr/bin/python3
# class to handle hotkeys key combos are: ctrl+shift+<key>
import pickle
import keyboard
import mouse

# here for reference while developing file IO
ex_binds = {
    'binds':
        {
        "ctrl+alt+b": "ß", 
        "ctrl+alt+a": "ä",
        "ctrl+alt+o": "ö", 
        "ctrl+alt+u": "ü", 
        "alt+a+shift": "Ä",
        "alt+o+shift": "Ö",
        "alt+u+shift": "Ü"
        },
    'config': 
        {
        'capitalize': False,
        }
}

def save_obj(obj, name):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, -1)
        
def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

class hkManager:
    def __init__(self,fname='keyBindReg.pkl') -> None:
        """
        summary: Object to manage hotkeys and bind them to functions.
        Hotkey callbacks are generics and call the write method with the target string.
        This example is for german characters on a US keyboard layout. 
        Capitalization is supported by replacing ctrl modifier with shift.
    
        """
        self.fname = fname
        self.config = ex_binds.copy()
        self.key_binds = self.config['binds']
        self.cap_binds = self.config['config']['capitalize']
        self.warning = False
        
    def __str__(self) -> str:
        # load the keybinds from the file
        return f'{load_obj(self.fname)}'
    
    def getBinds(self,exclude:list=[]):
        """returns a list of the keyBinds dict keys

        Args:
            exclude (list, optional): list of keys to exclude from the list. Defaults to [].

        Returns:
            list: list of keyBinds dict keys
        """
        return [key for key in self.key_binds.keys() if key not in exclude]
            
    def add_hotkeys(self, hotkeys:list):
        """adds hotkeys to the keyboard and mouse hooks

        Args:
            hotkeys (list): list of strings that are either:
                'key combos'|'mouse events' to hook.
        """
        for key in hotkeys:
            target = self.key_binds[key]
            keyboard.add_hotkey(key, self.write, args=[str(target)])
            # add a version with caps
            if self.cap_binds:
                self.add_caps_hotkey(key, target)
        # add the config hotkey here because its static and not a user defined hotkey
        keyboard.add_hotkey('win+ctrl', self.show_config)
        save_obj(self.key_binds, self.fname)

    def add_caps_hotkey(self, key, target):
        cap_hk = key.strip('ctrl+')+'+shift'
        self.key_binds[cap_hk] = target.upper()
        keyboard.add_hotkey(cap_hk, self.write, args=[str(target.upper())])
        
    def show_config(self):
        # launch the form with the keybinds
        # self.menu = subprocess.Popen(['python', 'form_generator.py', json.dumps(self.key_binds)])
        pass
        
    def remove_hotkeys(self, hotkeys:list):
        """removes hotkeys from the keyboard and mouse hooks

        Args:
            hotkeys (list): list of strings that are either:
                'key combos'|'mouse events' to unhook.
        """   
        for key in hotkeys:
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
    
def main():
    t = hkManager(fname='keyBindReg_german.pkl')
    t.add_hotkeys(t.getBinds(exclude=['ctrl+win']))
    # start the listener, 
    t.wait('ctrl+shift+q')
    # exit with ctrl+shift+q
    print(t)
    
if __name__ == "__main__":
    main()