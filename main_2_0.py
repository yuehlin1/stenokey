import keyboard as kb
from keyboard_2_0 import StenokeyMatcher, LiukeyMatcher
import time
import os
from typing import Dict

# TODO : After execution, the first liu word is not working
# TODO : Liu word doesn't work sometimes. maybe need two spaces to work.


class AbbrevLoader():
    "load abbrev files in the directory called abbrev"
    # TODO decide whether stock every word into a dictionary(memory burden), 
    # or return an iterable(I/O cost)
    
    def __init__(self):
        self.liu_dict = dict()
        self.steno_dict = dict()

    def load(self):
        os.chdir("abbrev")
        files = os.listdir()
        for file in files:
            if file.startswith("steno"):
                abbrev_type = "steno"
            elif file.startswith("liu"):
                abbrev_type = "liu"
            else:
                raise Exception("abbrev_type not understood")
            with open(file, "r", encoding='utf-8') as f:
                for line in f:
                    self.add_abbrev(line, abbrev_type)
        os.chdir("..")
    
    def add_abbrev(self, line, abbrev_type):
        line = line.replace('\n', '')
        abbrev, full_form = line.split(" ")
        abbrev = abbrev.lower()
        if abbrev_type == "steno":
            abbrev = ''.join(sorted(list(abbrev)))
            self.steno_dict[abbrev] = full_form
        elif abbrev_type == "liu":
            self.liu_dict[abbrev] = full_form
        else:
            raise Exception("abbrev type not understood")
    

class KeyboardSituation:
    
    def __init__(self, steno_dict, liu_dict):
        self.event_queue = []
        self.steno_dict = steno_dict
        self.liu_dict = liu_dict
    
    def __call__(self, kbe: kb.KeyboardEvent):
        self.event_queue.append(kbe)
        if kbe.name == 'space' and kbe.event_type == 'up':
            lm = LiukeyMatcher(self.event_queue)
            msg = lm.match(self.liu_dict)
            kb.write(msg)
            self.event_queue = []
            
        if self.get_n_key_pressed() == 0:
            sm = StenokeyMatcher(self.event_queue)
            msg = sm.match(self.steno_dict)
            kb.write(msg)
            if msg == '':
                self.event_queue = []
    
    def get_n_key_pressed(self):
        n = 0
        for kbe in self.event_queue:
            if kbe.event_type == 'up':
                n-=1
            else:
                n+=1
        return n
        
def main():
    av = AbbrevLoader()
    av.load()
    STENO_DICT = av.steno_dict
    LIU_DICT = av.liu_dict
    print(LIU_DICT)
    ks = KeyboardSituation(STENO_DICT, LIU_DICT)
    kb.hook(ks)
    time.sleep(50)
    

if __name__ == "__main__":
    main()
    # dk return kreturn 蝸  蝸 牛 nr return return 蝸