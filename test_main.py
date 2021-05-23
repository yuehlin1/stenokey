import keyboard
import time
from main import KeyboardSituation, main
from dataclasses import dataclass
 
# class MyKeyboardEvent():
#     def __init__(self, name, event_type):
#         self.name = name
#         self.event_type = event_type
@dataclass
class MyKeyboardEvent():
    name : str
    event_type : str

         


if __name__ == "__main__":
    events = map(MyKeyboardEvent, ["r", "n", "r", "n"], ["down", "down", "up", "up"])
    def test_main(ks: KeyboardSituation):
        time.sleep(3)
        for event in events:
            ks(event) 
            # has the same effect of keyboard.hook(ks),
            # which calls ks(event) whenever a key is pressed/released
    main(on_test = test_main)
