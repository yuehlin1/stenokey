import time
import keyboard
import logging
logging.basicConfig(level=logging.WARNING)
# logging.basicConfig(level=logging.DEBUG)


from abbrev_loader import AbbrevLoader
from stenokey_matcher import StenokeyMatcher
from liukey_matcher import LiukeyMatcher
from manager import CombokeyToggleManager

from gui import GUI



def main(wait_for=5):
    sm = StenokeyMatcher(loader=AbbrevLoader())
    lm = LiukeyMatcher(loader=AbbrevLoader())
    mng = CombokeyToggleManager(sm, lm)
    mng.toggle_liu()
    mng.toggle_liu()
    time.sleep(wait_for)
    
class StenoHotkeyManager:
    def __init__(self, app):
        self.app = app
        
    def __call__(self, kbe):
        if kbe.name == "shift" and kbe.event_type == "up": # if shift is the only one being pressed
            return self.app.stenokey_button.invoke()
    
def main_gui():
    sm = StenokeyMatcher(loader=AbbrevLoader())
    lm = LiukeyMatcher(loader=AbbrevLoader())
    mng = CombokeyToggleManager(sm, lm)
    app = GUI(mng)
    shm = StenoHotkeyManager(app)
    keyboard.hook(shm)
    
    app.toggle_show_gui_hotkey_set("ctrl+space")
    
    
    
    
    app.mainloop()
    
if __name__ == "__main__":
    # wait_for=1e6
    # main(wait_for)
    main_gui()

