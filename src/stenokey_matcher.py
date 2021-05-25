import keyboard
import logging

# TODO when combining with liukey, steno doesn't always work
    
class StenokeyMatcher:
    VALID_NAME = set('1234567890-=qwertyuiop[]asdfghjkl;\'zxcvbnm,./\\')
    VALID_NAME.add("space")
    
    def __init__(self, steno_dict=None, loader=None, test_mode=False):
        self.event_queue = []
        self.test_mode = test_mode # when in test mode, don't send backspaces
        
        if loader is not None:
            loader.load()
            self.STENO_DICT = loader.steno_dict
        elif steno_dict is not None:
            self.STENO_DICT = steno_dict
        else:
            self.STENO_DICT = dict()
            logging.info("No loader or steno_dict is used")
    
    def __call__(self, kbe: keyboard.KeyboardEvent):
        if kbe.name in self.VALID_NAME:
            self.event_queue.append(kbe)
            
        if self.get_n_key_pressed() == 0:
            msg = self.get_match()
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
    
    def get_backspaces(self, abbrev):
        if self.test_mode:
            return ''
        else:
            return '\b'*len(abbrev)
    
    def get_match(self):
        keys_pressed = sorted(set(map(lambda kbe: kbe.name, self.event_queue)))
        abbrev = ''.join(keys_pressed)
        if abbrev in self.STENO_DICT.keys():
            return self.get_backspaces(abbrev) +  self.STENO_DICT[abbrev]
        else:
            return ''
        
    def hook(self):
        keyboard.hook(self)
        