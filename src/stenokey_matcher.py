import keyboard
import logging

    
class StenokeyMatcher:
    VALID_NAME = set('1234567890-=qwertyuiop[]asdfghjkl;\'zxcvbnm,./\\')
    THRESHOLD_OVERLAP_2 = 0.6
    THRESHOLD_OVERLAP_3 = 0.2
    
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
        logging.debug("steno call")
        logging.debug(self.event_queue)
        if kbe.name in self.VALID_NAME:
            self.event_queue.append(kbe)
        else:
            self.event_queue = []
            
        if self.get_n_key_pressed() == 0:
            if self.is_stenokey_pattern(): # to distinguish typing too fast and intentional combo
                msg = self.get_match()
                keyboard.write(msg)
            self.event_queue = []
    
    def is_stenokey_pattern(self):
        if not self.all_get_pressed_at_the_same_time():
            return False
        elif len(self.event_queue) == 4:
            return self.cal_overlap_ratio2() > self.THRESHOLD_OVERLAP_2
        elif len(self.event_queue) == 6:
            return self.cal_overlap_ratio3() > self.THRESHOLD_OVERLAP_3
        else:
            return True
        
    def all_get_pressed_at_the_same_time(self):
        # can filter out -----
        #                   -----
        #                      -----
        #                         -----
        #                             -----
        # something like this. This should be normal key, not combo key
        level = 0
        for kbe in self.event_queue:
            if kbe.event_type == 'up':
                break
            level+=1
        return level*2 == len(self.event_queue)
        
    def cal_overlap_ratio2(self):
        [down1, down2, up1, up2] = self.event_queue
        # case 1                |     else
        # ------                |    ------
        #  ------               |     ----
        # calculate overlap     |  is surely stenokey
        if down1.name == up1.name:
            return (up1.time-down2.time)/(up2.time-down1.time) # calculate overlap
        else:
            return 1 # is surely stenokey
    
    def cal_overlap_ratio3(self):
        #     case 1            |       case 2
        #  --------             |      -------
        #    --------           |       -----
        #      --------         |         ------
        #  calculate overlap    |     calculate overlap
        # since filtered out by all_get_passed_at_the_same_time it should be fine
        [down1, down2, down3, up1, up2, up3] = self.event_queue
        return (up1.time-down3.time)/(up3.time-down1.time)
        # just calculate the ratio should be fine since the threshold should be lower

    
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
        