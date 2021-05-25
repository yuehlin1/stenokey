import time
import keyboard
import logging
logging.basicConfig(level=logging.WARNING)


from abbrev_loader import AbbrevLoader
from stenokey_matcher import StenokeyMatcher
from liukey_matcher import LiukeyMatcher



def main(wait_for=5):
    sm = StenokeyMatcher(loader=AbbrevLoader())
    lm = LiukeyMatcher(loader=AbbrevLoader())
    sm.hook()
    lm.hook()
    time.sleep(wait_for)
    
    
if __name__ == "__main__":
    wait_for=1e6
    main(wait_for)

