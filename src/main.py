import time
import keyboard
import logging
logging.basicConfig(level=logging.DEBUG)


from abbrev_loader import AbbrevLoader
from stenokey_matcher import StenokeyMatcher


# changelog : Liukey functionality removed for simplicity

def main(wait_for=5):
    sm = StenokeyMatcher(loader=AbbrevLoader())
    sm.hook()
    time.sleep(wait_for)
    
    
if __name__ == "__main__":
    wait_for=1e6
    main(wait_for)

