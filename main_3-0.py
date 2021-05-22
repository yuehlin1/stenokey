from re import I
import keyboard as kb
import time
import os
from typing import Dict

# changelog : Liukey functionality removed for simplicity

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
    

class StenokeyMatcher():
    def __init__(self, event_queue):
        self.event_queue = event_queue
        
    def match(self, steno_dict):
        keys_pressed = sorted(set(map(lambda kbe: kbe.name, self.event_queue)))
        abbrev = ''.join(keys_pressed)
        if abbrev in steno_dict.keys():
            return '\b'*len(abbrev)+steno_dict[abbrev]
        else:
            return ''
    
    # def is_triggered(self):
    #     return self.get_n_key_pressed() == 0
        
        
    # def get_n_key_pressed(self):
    #     n = 0
    #     for kbe in self.event_queue:
    #         if kbe.event_type == "down":
    #             n+=1
    #         elif kbe.event_type == "up":
    #             n-=1
    #         else:
    #             raise Exception("Event type not up nor down")
    #     return n
    
    
class KeyboardSituation:
    VALID_NAME = set('1234567890-=qwertyuiop[]asdfghjkl;\'zxcvbnm,./\\')
    VALID_NAME.add("space")
    
    def __init__(self, steno_dict):
        self.event_queue = []
        self.steno_dict = steno_dict
    
    def __call__(self, kbe: kb.KeyboardEvent):
        if kbe.name in self.VALID_NAME:
            self.event_queue.append(kbe)
            
        if self.get_n_key_pressed() == 0:
            sm = StenokeyMatcher(self.event_queue)
            msg = sm.match(self.steno_dict)
            kb.write(msg)
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
    ks = KeyboardSituation(STENO_DICT)
    kb.hook(ks)
    time.sleep(50)
    

if __name__ == "__main__":
    l = []
    try:
        main()
    except KeyboardInterrupt:
        print(l)
