# In this file, a notepad-like environment is coded with pygame. You can
# - type words using english keyboard (at the position of cursor)
# - shift + word becomes uppercase
# - capslock has no effect
# - enter, backspace work (at the position of cursor)
# - cursor only supports left and right, up and down has no effect
# - combo keys are implemented
#   - TODO recreate local_keylist so that it takes in time argument as well
#     so that we can distinguish combo keys from typing too fast
#   - TODO update_global_textlist_and_cursor needs to be revisited. It shouldn't
#     visiting every key in local_keylist at a time, rather look at the whole list
# update 3.0 : Refactoring succeeded. Now there are two classes, Notepad and KeyPressHandler
#   Notepad can access words being written and the cursor and update them. 
#   KeyPressHandler can detect pressed key and update notepad's key_queue

import pygame
from event_key_char_map import event_key_char_map, event_key_char_map_shift
from key_stroke_combo_text_map import keystroke_combo_text_map as combo

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((500, 500))
font = pygame.font.SysFont("arial", 40)


class Notepad(object):
    "this class can access words being written and the cursor"
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.global_textlist = []
        self.queue = []
        self.cursor_x = 0
        self.shift_mode = False
        self.ctrl_mode = False
        self.define_mode = False

    def write_down(self, string): # at the cursor
        self.global_textlist.insert(self.cursor_x, string)
        self.cursor_x += 1

    def press_backspace(self):
        try:
            self.global_textlist.pop(self.cursor_x-1)
            self.cursor_x -= 1
            if self.ctrl_mode and self.global_textlist[self.cursor_x-1] != ' ':
                self.press_backspace()
        except IndexError:
            pass

    def press_enter(self):
        self.global_textlist.insert(self.cursor_x, "\n")
        self.cursor_x += 1

    def press_left(self):
        try:
            self.cursor_x -= 1
            if self.ctrl_mode and self.global_textlist[self.cursor_x-1] != ' ':
                self.press_left()
        except IndexError:
            pass

    def press_right(self):
        try:
            if self.cursor_x  < len(self.global_textlist):
                self.cursor_x += 1
            if self.ctrl_mode and self.global_textlist[self.cursor_x+1] != ' ':
                self.press_right()
        except IndexError:
            pass

    def draw_screen(self, blink):
        self.screen.fill((255, 255, 255))
        global_text = self.get_text(blink)
        if global_text is not None:
            self.draw_text(global_text)
        pygame.display.update()

    def draw_text(self, text):
        self._blit_text(text, pos:=(0,0))

    def _blit_text(self, text, pos, color=pygame.Color('black')):
        surface = self.screen
        font = self.font

        """render multiple line of text"""
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.   

    def get_text(self, blink):
        global_textlist, cursor_x = self.global_textlist, self.cursor_x
        if blink:
            global_text = ''.join(global_textlist[:cursor_x]+['▯']+global_textlist[cursor_x+1:])
        else:
            global_text = ''.join(global_textlist)
        return global_text
    
    def press_one_key(self, keystroke):
        if keystroke == "left":
            self.press_left()
        elif keystroke == "right":
            self.press_right()
        elif keystroke == 'enter':
            self.press_enter()
        elif keystroke == 'backspace':
            self.press_backspace()
        else:
            self.write_down(keystroke)

    def update(self):
        # release combo. Release the keystrokes stocked in self.queue
        if (keys:=self.queue).__len__() == 1:
            self.press_one_key(keys[0])
        elif (dict_key := tuple(sorted(self.queue))) in combo.keys():
            for keystroke in combo[dict_key]:
                self.press_one_key(keystroke)
        else:
            for keystroke in self.queue:
                self.press_one_key(keystroke)
        self.collect()

    def collect(self):
        self.shift_mode, self.ctrl_mode = False, False
        queue = self.queue.copy()
        self.queue = []
        return queue


class KeyPressHandler(object):
    "this class can access the key being pressed and do thing on notebook"
    def __init__(self):
        self.hotkey = []
        self.content = []

    def apply_to(self, event, notepad):
        self.event = event
        SHIFT = 1073742049
        CTRL = 1073742048
        BACKSPACE = 8
        if self.event.type == pygame.KEYDOWN:
            if self.event.key == SHIFT:
                notepad.shift_mode = True
            elif self.event.key == CTRL:
                notepad.ctrl_mode = True
            # else:
            #     if notepad.ctrl_mode and self.event.key == pygame.K_d and not notepad.define_mode: # use to add new hotkeys
            #         print("Defining custom hotkey. Please enter the new hotkey, then press Ctrl+D again.")
            #         notepad.define_mode = True
            #         notepad.collect()

            #     elif notepad.ctrl_mode and self.event.key == pygame.K_d and notepad.define_mode:
            #         print("Custom hotkey received. Please enter its definition. then press Ctrl+F. ")
            #         self.hotkey = notepad.collect()
                    


            #     elif notepad.ctrl_mode and self.event.key == pygame.K_f: # end define mode
            #         print("Definition received. Quitting define mode.")
            #         self.content = notepad.collect()
                    
            #         # content = notepad.update()
            #         combo[tuple(sorted(self.hotkey))] = ''.join(self.content) 
            #         notepad.define_mode = False
                    
            elif notepad.shift_mode:
                stroke = event_key_char_map_shift[self.event.key]
                notepad.queue.append(stroke)
            else:
                stroke = event_key_char_map[self.event.key]
                notepad.queue.append(stroke)
                

        if self.get_n_key_pressed() == 0 and not notepad.define_mode: # time to resolve notepad.local_keylist
            notepad.update()
            
    def get_n_key_pressed(self):
        return sum(iter(pygame.key.get_pressed()))


if __name__ == "__main__":
    # TODO select a paragraph with shift + directional
    # TODO cursor with up down command
    clock = pygame.time.Clock()
    notepad = Notepad(screen, font)
    handler = KeyPressHandler()
    run = True
    i=0
    while run:
        i+=1
        clock.tick(FPS:=60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            handler.apply_to(event, notepad)
        notepad.draw_screen(blink:=(i//30)%2)
    pygame.quit()

