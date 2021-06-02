import time
import keyboard
import logging
logging.basicConfig(level=logging.WARNING)
# logging.basicConfig(level=logging.DEBUG)


from abbrev_loader import AbbrevLoader
from stenokey_matcher import StenokeyMatcher
from liukey_matcher import LiukeyMatcher

from gui import App



def main(wait_for=5):
    sm = StenokeyMatcher(loader=AbbrevLoader())
    lm = LiukeyMatcher(loader=AbbrevLoader())
    sm.hook()
    lm.hook()    
    time.sleep(wait_for)
    
def main_gui():
    sm = StenokeyMatcher(loader=AbbrevLoader())
    lm = LiukeyMatcher(loader=AbbrevLoader())
    app = App(sm=sm, lm=lm)
    # keyboard.add_hotkey('shift', app.stenokey_button.invoke)
    app.mainloop()
    
if __name__ == "__main__":
    # wait_for=1e6
    # main(wait_for)
    main_gui()

