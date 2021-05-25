import keyboard
import time
import os
import logging

logging.basicConfig(level=logging.DEBUG)

# changelog : Liukey functionality removed for simplicity

class AbbrevLoader():
    "load abbrev files in the directory called abbrev"
    # TODO decide whether stock every word into a dictionary(memory burden), 
    # or return an iterable(I/O cost)
    
    def __init__(self):
        self.liu_dict = dict()
        self.steno_dict = dict()

    def load(self, file_dir='abbrev'):
        current_dir = os.getcwd()
        os.chdir(file_dir)
        files = os.listdir()
        for file in files:
            if file.startswith("steno"):
                abbrev_type = "steno"
            elif file.startswith("liu"):
                abbrev_type = "liu"
            else:
                raise Exception("file abbrev_type not understood")
            with open(file, "r", encoding='utf-8') as f:
                for line in f:
                    self.add_abbrev(line, abbrev_type)
        os.chdir(current_dir)
    
    def add_abbrev(self, line:str, abbrev_type):
        line = line.replace('\n', '')
        pos = line.find(' ')
        abbrev = line[:pos]
        full_form = line[pos+1:]
        abbrev = abbrev.lower()
        if abbrev_type == "steno":
            abbrev = ''.join(sorted(list(abbrev)))
            self.steno_dict[abbrev] = full_form
        elif abbrev_type == "liu":
            self.liu_dict[abbrev] = full_form
        else:
            raise Exception("abbrev type not understood")
    
    
class StenokeyMatcher:
    VALID_NAME = set('1234567890-=qwertyuiop[]asdfghjkl;\'zxcvbnm,./\\')
    VALID_NAME.add("space")
    
    def __init__(self, steno_dict):
        self.event_queue = []
        self.STENO_DICT = steno_dict
    
    def __call__(self, kbe: keyboard.KeyboardEvent):
        if kbe.name in self.VALID_NAME:
            self.event_queue.append(kbe)
            
        if self.get_n_key_pressed() == 0:
            msg = self.match()
            keyboard.write(msg)
            self.event_queue = []
    
    def get_n_key_pressed(self):
        n = 0
        for kbe in self.event_queue:
            if kbe.event_type == 'up':
                n-=1
            else:
                n+=1
        return n
    
    def match(self):
        keys_pressed = sorted(set(map(lambda kbe: kbe.name, self.event_queue)))
        abbrev = ''.join(keys_pressed)
        if abbrev in self.STENO_DICT.keys():
            return '\b'*len(abbrev) +  self.STENO_DICT[abbrev]
        else:
            return ''
        
def main(wait_for=5):
    av = AbbrevLoader()
    av.load()
    STENO_DICT = av.steno_dict
    sm = StenokeyMatcher(STENO_DICT)
    keyboard.hook(sm)
    
    time.sleep(wait_for)
    

if __name__ == "__main__":
    wait_for=5
    main(wait_for)

