from tkinter.constants import SCROLL
import keyboard
import logging
import pyautogui as ag

    
class VimiumMatcher:
    LENGTH, HEIGHT = ag.size()
    
    def __init__(self):
        self.load()
    
    def load(self):
        pass
    
    def matrix2position(self, i, j):
        """calculate the (i, j)th keyboard grid's corresponding pixel position. The grid is 4 by 3 for now."""
        return self.LENGTH*(i/4+1/8), self.HEIGHT*(j/3+1/6)
    
    def __call__(self, kbe: keyboard.KeyboardEvent):
        # TODO alternative for backspacing. 
        # TODO handle directional keys. Typing 'up' not only moves mouse but also acts as keyboard input. 
        
        # grid2matrix = {"q":(0, 0), "w":(1, 0)}
        
        if kbe.event_type != "down":
            return None
        
        grids = 'qwerasdfzxcv'
        matrices = [(i, 0) for i in range(4)] + [(i, 1) for i in range(4)] + [(i, 2) for i in range(4)]
        grid2matrix = dict(zip(grids, matrices))
        
        if kbe.name not in list('qwerasdfzxcv'):
            pass
        else:
            indices = grid2matrix[kbe.name]
            destination = self.matrix2position(*indices)
            keyboard.send('\b')
            ag.moveTo(*destination, duration=0.2)
            
        
        scroll_dict = dict(zip(list("yhtg5b"), [50, -50, 250, -250, 1000, -1000] ))

        
        if kbe.name.lower() not in "yhtg5b":
            pass
        else:
            keyboard.send('\b')
            ag.scroll(scroll_dict[kbe.name.lower()])

            
        if kbe.name.lower()  == 'u'  :
            keyboard.send('\b')
            ag.click()
            
        if kbe.name.lower()  == 'o'  :
            keyboard.send('\b')
            ag.rightClick()
        
        
        STEP = 100
        if kbe.name in list("IJKL"):
            keyboard.send('\b')
        if kbe.name in ['up', 'I']  :
            ag.moveRel(0, -1*STEP, duration=0)
        elif kbe.name in ['down', "K"]  :
            ag.moveRel(0, 1*STEP, duration=0)
        elif kbe.name in ['left', "J"]  :
            ag.moveRel(-1*STEP, 0, duration=0)
        elif kbe.name in ['right', "L"]  :
            ag.moveRel(1*STEP, 0, duration=0)
        
            
            
        STEP = 10
        if kbe.name in "ijkl":
            keyboard.send("\b")
        if kbe.name  == 'i'  :
            ag.moveRel(0, -1*STEP, duration=0)
        elif kbe.name  == 'k'  :
            ag.moveRel(0, 1*STEP, duration=0)
            
        elif kbe.name == 'j'  :
            ag.moveRel(-1*STEP, 0, duration=0)

        elif kbe.name == 'l'  :
            ag.moveRel(1*STEP, 0, duration=0)
            
            
        

        
        return None
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
            
            
    def hook(self):
        self.handler = keyboard.hook(self)
        # self.handler = {}
        # for key in self.VALID_NAME | self.USEFUL_KEY:
        #     self.handler[key] = keyboard.hook_key(key, self)
        
        
    def unhook(self):
        # for key in self.VALID_NAME | self.USEFUL_KEY:
        #     keyboard.unhook_key(key)
        keyboard.unhook(self.handler)
        
    