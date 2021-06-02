class CombokeyToggleManager():
    def __init__(self, sm, lm):
        self.sm = sm
        self.lm = lm
        self.stenokey_on = False
        self.liukey_on = False
        
    def reload(self):
        self.sm.load()
        self.lm.load()
        
    def toggle_steno(self):
        self.stenokey_on = not self.stenokey_on
        if self.stenokey_on:
            self.sm.hook()
        else:
            self.sm.unhook()
            
    def toggle_liu(self):
        self.liukey_on = not self.liukey_on
        if self.liukey_on:
            self.lm.hook()
        else:
            self.lm.unhook()
            
    def deactivate(self):
        self.stenokey_was_on = self.stenokey_on
        self.liukey_was_on = self.liukey_on
        if self.stenokey_was_on:
            self.toggle_steno()
        if self.liukey_was_on:
            self.toggle_liu()
    
    def reactivate(self):
        if self.stenokey_was_on:
            self.toggle_steno()
        if self.liukey_was_on:
            self.toggle_liu()
        
        