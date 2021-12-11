import time
import keyboard
import logging
logging.basicConfig(level=logging.WARNING)
# logging.basicConfig(level=logging.DEBUG)


from abbrev_loader import AbbrevLoader
from stenokey_matcher import StenokeyMatcher
from liukey_matcher import LiukeyMatcher
from manager import CombokeyToggleManager
from single_hotkey import SingleHotkey

from gui import GUI



def main(wait_for=5):
    sm = StenokeyMatcher(loader=AbbrevLoader())
    lm = LiukeyMatcher(loader=AbbrevLoader())
    mng = CombokeyToggleManager(sm, lm)
    mng.toggle_steno()
    mng.toggle_liu()
    time.sleep(wait_for)
    

    
def main_gui():
    sm = StenokeyMatcher(loader=AbbrevLoader())
    lm = LiukeyMatcher(loader=AbbrevLoader())
    mng = CombokeyToggleManager(sm, lm) # manager controls sm, lm
    app = GUI(mng) # app controls manager
    shm = SingleHotkey(hotkey="shift", onclick=app.stenokey_button.invoke) # hotkey controls app
    shm.hook()
    app.toggle_show_gui_hotkey_set("ctrl+space")
    keyboard.add_hotkey("alt+`", app.liukey_button.invoke)
    
    
    
    
    app.mainloop()
    
if __name__ == "__main__":
    # wait_for=1e6
    # main(wait_for)
    main_gui()

