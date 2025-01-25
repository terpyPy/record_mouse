from hotkeys import hkManager

class German_AHK(hkManager):
    def __init__(self, file:str):
        super().__init__(file)
        
    def esset(self):
        print('ß')
        # 
        self.write('ß')
        
    def a_umlaut(self):
        print('ä')
        # 
        self.write('ä')
        
    def o_umlaut(self):
        print('ö')
        # 
        self.write('ö')
        
    def u_umlaut(self):
        print('ü')
        # 
        self.write('ü')
        
    def test_char(self):
        # test bind
        print('not bound')
        
    # create __repr__ method to print all function names
    def __repr__(self):
        """returns a string representation of the class, can be used to recreate the keyReg """
        namespae =[
                    self.esset.__name__,
                    self.a_umlaut.__name__, 
                    self.o_umlaut.__name__, 
                    self.u_umlaut.__name__,
                    self.test_char.__name__
                    ]
        # make a dictionary with getbinds() and the function names
        d = dict(zip(self.getBinds(), namespae))
        return f'{d}'
    
hk = German_AHK(file='keyBindReg_german.json')
# old way of binding functions to hotkeys
hk.add_hotkeys(hk.getBinds())
# start the listener, exit with ctrl+shift+q
hk.wait('ctrl+shift+q')
print(hk)