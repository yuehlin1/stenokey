import keyboard
import time
import os

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
    

class StenokeyMatcher():
    def __init__(self, event_queue):
        self.event_queue = event_queue
        keys_pressed = sorted(set(map(lambda kbe: kbe.name, self.event_queue)))
        self.abbrev = ''.join(keys_pressed)
        
    def get_backspaces(self):
        return '\b'*len(self.abbrev)
    
    def get_full_text(self, steno_dict):
        return steno_dict[self.abbrev]
        
    def match(self, steno_dict):
        # keys_pressed = sorted(set(map(lambda kbe: kbe.name, self.event_queue)))
        # abbrev = ''.join(keys_pressed)
        abbrev = self.abbrev
        if abbrev in steno_dict.keys():
            # return '\b'*len(abbrev)+steno_dict[abbrev]
            return self.get_backspaces() + self.get_full_text(steno_dict)
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
    STENO_DICT = dict()
    
    
    def __init__(self):
        self.event_queue = []
    
    def __call__(self, kbe: keyboard.KeyboardEvent):
        if kbe.name in self.VALID_NAME:
            self.event_queue.append(kbe)
            
        if self.get_n_key_pressed() == 0:
            sm = StenokeyMatcher(self.event_queue)
            msg = sm.match(self.STENO_DICT)
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
        
def main(on_test=None):
    av = AbbrevLoader()
    av.load()
    STENO_DICT = av.steno_dict
    ks = KeyboardSituation()
    ks.STENO_DICT = STENO_DICT
    keyboard.hook(ks)
    if on_test:
        on_test(ks)
    time.sleep(50)
    

if __name__ == "__main__":
    main()

