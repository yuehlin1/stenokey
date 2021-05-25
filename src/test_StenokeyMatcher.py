from abbrev_loader import AbbrevLoader
from stenokey_matcher import StenokeyMatcher
from dataclasses import dataclass
import keyboard
import time

@dataclass
class MyKeyboardEvent:
    name : str
    event_type : str

def create_events(string):
    n = len(string)
    # events = map(MyKeyboardEvent, ['r', 'n', 'r', 'n'], ['down', 'down', 'up', 'up'])
    events = map(MyKeyboardEvent, 
                 [string[i%n] for i in range(2*n)], 
                 ["down"]*n+["up"]*n)
    return events

if __name__ == "__main__":
    combo = "ifn"
    events = create_events(combo)
    
    sm = StenokeyMatcher(loader = AbbrevLoader(), test_mode = True)
    
    print(f"Sending {combo} in 5 sec. Please move to a texting environment. ")
    time.sleep(5)
    for event in events:
        sm(event)
        time.sleep(0.3)
    print("sent")
    time.sleep(5)