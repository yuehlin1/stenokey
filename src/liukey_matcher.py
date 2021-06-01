import keyboard
import logging

    
class LiukeyMatcher:
    VALID_NAME = set('abcdefghijklmnopqrstuvwxyz,.')
    
    def __init__(self, liu_dict=None, loader=None, test_mode=False):
        self.event_queue = []
        self.test_mode = test_mode # when in test mode, don't send backspaces
        
        self._liu_dict = liu_dict
        self._loader = loader
        
        self.load()
    
    def load(self):
        loader = self._loader
        liu_dict = self._liu_dict
        if loader is not None:
            loader.load()
            self.LIU_DICT = loader.liu_dict
        elif liu_dict is not None:
            self.LIU_DICT = liu_dict
        else:
            self.LIU_DICT = dict()
            logging.info("No loader or liu_dict is used")
    
    def __call__(self, kbe: keyboard.KeyboardEvent):
        # TODO handle backspace
        if kbe.event_type == 'up':
            return None
        
        if kbe.name in self.VALID_NAME:
            self.event_queue.append(kbe)
            
        elif kbe.name == 'space':
            msg = self.get_match()
            keyboard.write(msg)
            self.event_queue = []
        
        elif kbe.name == 'backspace':
            try:
                self.event_queue.pop()
            except IndexError:
                pass
            
        else: # kbe.name not valid
            self.event_queue = []
            
            
        
    
    def get_backspaces(self, abbrev):
        return '\b'*(1+len(abbrev))
    
    def get_match(self):
        filtered_events = filter(lambda kbe: kbe.event_type == 'down', self.event_queue)
        keys_pressed = map(lambda kbe: kbe.name, filtered_events)
        abbrev = ''.join(keys_pressed)
        logging.debug(abbrev)
        if abbrev in self.LIU_DICT.keys():
            return self.get_backspaces(abbrev) +  self.LIU_DICT[abbrev]
        else:
            return ''
        
    def hook(self):
        self.handler = keyboard.hook(self)
        
    def unhook(self):
        keyboard.unhook(self.handler)