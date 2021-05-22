from typing import Dict
import keyboard
import os

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
        # print(abbrev)
        if abbrev in steno_dict.keys():
            return '\b'*len(abbrev)+steno_dict[abbrev]
        else:
            return ''
    
    def is_triggered(self):
        return self.get_n_key_pressed() == 0
        
        
    def get_n_key_pressed(self):
        n = 0
        for kbe in self.event_queue:
            if kbe.event_type == "down":
                n+=1
            elif kbe.event_type == "up":
                n-=1
            else:
                raise Exception("Event type not up nor down")
        return n
        
class LiukeyMatcher():
    def __init__(self, event_queue):
        self.event_queue = event_queue
        
    def is_triggered(self):
        kbe = self.event_queue[-1]
        return kbe.name == "space" and kbe.event_type == "up"
    
    def match(self, liu_dict):
        only_key_down = filter(lambda x: x.event_type == "down" and x.name != "space",
                               self.event_queue)
        only_key_down = map(lambda x: x.name, only_key_down)
        
        abbrev = ''.join(only_key_down)
        if abbrev in liu_dict.keys():
            return '\b'*(1+len(abbrev))+liu_dict[abbrev]
        else:
            return ''
    
        
# class CqosjLiu():
#     def __init__(self, event_queue):
#         self.event_queue = event_queue
        
    # def look_up(self, abbrev_dict):
        
    
    
    
        
            
    

def main():
    av = AbbrevLoader()
    av.load()
    # cqosj = CqosjLiu()
    # cqosj.define_abbrev(av.abbrev_dict)
    # cqosj.listen_shift()
    
    print(av.liu_dict)
    print(av.steno_dict)
    # time.sleep(5)
        
if __name__ == "__main__":
    main()