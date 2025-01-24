#!/usr/bin/python3
# class to handle hotkeys key combos are: ctrl+shift+<key> 
import keyboard
import mouse
import json

class hkManager:
    def __init__(self,file='keyBindReg.json') -> None:
        """
        summary: object to manage hotkeys and bind them to functions,
        the numeric values will map to the functions listed below, in order.\n example:
        {'ctrl+shift+1': function name}\n 
    
        """
        self.file = file
        self.keyBinds = json.load(open(file, 'r'))
        self.warning = False
        
    def __str__(self) -> str:
        return f'hotkeys registered in {self.file}:\n{self.keyBinds}'
        
    def getBinds(self,exclude:list=[]):
        """returns a list of the keyBinds dict keys

        Args:
            exclude (list, optional): list of keys to exclude from the list. Defaults to [].

        Returns:
            list: list of keyBinds dict keys
        """
        return [key for key in self.keyBinds.keys() if key not in exclude]
        
    def init_funcs_to_dict(self, funcs:list):
        """DEPRECATED: maps the functions to the keyBinds dict

        Args:
            funcs (list): list of functions to map to the keyBinds dict
        """
        print('DEPRECATED: function names are now read from the keyBindReg.json file.\n')
        self.warning = True
        self.keyBinds = dict(zip(self.keyBinds.keys(), funcs))
        
    def add_hotkeys(self, hotkeys:list):
        """adds hotkeys to the keyboard and mouse hooks

        Args:
            hotkeys (list): list of strings that are either:
                'key combos'|'mouse events' to hook.
        """
        for key in hotkeys:
            target = getattr(self, self.keyBinds[key])
            keyboard.add_hotkey(key, target)
            
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
        
    # make a wrapper for mouse.is_pressed(button='')
    def is_pressed(self, button):
        return mouse.is_pressed(button=button)
    
    def is_Held(self, keysDown:str):
       return keyboard.is_pressed(keysDown)
   
    def wait(self, keysDown:str):
        return keyboard.wait(keysDown)

    def write(self, text:str):
        return keyboard.write(text)
       
    
if __name__ == "__main__":
    t = hkManager(file='keyBindReg_german.json')
    # t.add_hotkeys(t.getBinds())
    # start the listener, exit with ctrl+shift+q
    # t.wait('ctrl+shift+q')
    print(t)