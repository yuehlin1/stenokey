import keyboard

class SingleHotkey:
    def __init__(self, hotkey, onclick):
        self.hotkey = hotkey
        self.onclick = onclick
        self.last_kbe = None
        
    def __call__(self, kbe):
        if self.last_kbe is None:
            pass
        elif kbe.name == self.last_kbe.name == self.hotkey and kbe.event_type == "up":
            self.onclick()
        self.last_kbe = kbe
    
    def hook(self):
        keyboard.hook(self)
