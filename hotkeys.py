#!/usr/bin/python3
# class to handle hotkeys key combos are: ctrl+shift+<key> 
import keyboard
import mouse

class hkManager:
    def __init__(self) -> None:
        """
        summary: object to manage hotkeys and bind them to functions,
        the numeric values will map to the functions listed below, in order.\n
        1.('ctrl+shift+q', state.stop)\n 
        2.('ctrl+shift+p', playing)\n
        3.('ctrl+shift+s', saveRecording)\n
        4.(state.onLeftClick)
        """
        self.keyBinds = {'ctrl+shift+q': 1,
                         'ctrl+shift+p': 2,
                         'ctrl+shift+s': 3,
                         'leftClick': 4}
        
    def init_funcs_to_dict(self, funcs:list):
        """maps the functions to the keyBinds dict

        Args:
            funcs (list): list of functions to map to the keyBinds dict
        """
        self.keyBinds = dict(zip(self.keyBinds.keys(), funcs))
        
    def add_hotkeys(self, hotkeys:list):
        """adds hotkeys to the keyboard and mouse hooks

        Args:
            hotkeys (list): list of strings that are either:
                'key combos'|'mouse events' to hook.
        """
        if 'leftClick' in hotkeys:
            mouse.on_click(self.keyBinds['leftClick'])
            hotkeys.remove('leftClick')
        
        for key in hotkeys:
            keyboard.add_hotkey(key, self.keyBinds[key])
            
    def remove_hotkeys(self, hotkeys:list):
        """removes hotkeys from the keyboard and mouse hooks

        Args:
            hotkeys (list): list of strings that are either:
                'key combos'|'mouse events' to unhook.
        """
        if 'leftClick' in hotkeys:
            mouse.unhook_all()
            hotkeys.remove('leftClick')
        
        for key in hotkeys:
            keyboard.remove_hotkey(key)
    
    def kill_all(self):
        """unhooks all hotkeys from the keyboard and mouse hooks"""
        keyboard.unhook_all()
        mouse.unhook_all()
        
    # make a wrapper for mouse.is_pressed(button='')
    def is_pressed(self, button):
        return mouse.is_pressed(button=button)