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

import pygame
from event_key_char_map import event_key_char_map, event_key_char_map_shift
from key_stroke_combo_text_map import keystroke_combo_text_map as combo

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((500, 500))


local_keylist = []
global_textlist = []
font = pygame.font.SysFont("arial", 40)
cursor_x = 0 # it should be between 0 and len(global_textlist)


def get_n_key_pressed():
    return sum(iter(pygame.key.get_pressed()))

def handle_keydown(event):
    global cursor_x
    print(event.key)
    if False:
        pass
    else:
        local_keylist.append(event.key)
    
def handle_keyup(event):
    pass

def handle_keypress(event):
    if event.type == pygame.KEYDOWN:
        handle_keydown(event) # do something to the list
        # print("store the pressed key and pressed frame in a list")

    if event.type == pygame.KEYUP:
        handle_keyup(event) # do something to the list
        # print("release the list to display screen")

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
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

def draw_text(global_text):
    # TODO optimize. Don't parse text again and again. Change key in type to be a list directly
    blit_text(screen, global_text, pos:=(0,0), font)

def handle_one_key(keystroke, shift_mode, ctrl_mode):
    # TODO take shift into account
    global global_textlist, cursor_x
    # keystroke = event_key_char_map_shift[key] if shift_mode else event_key_char_map[key]
    try:
        if keystroke == "left":
            cursor_x -= 1
            if ctrl_mode and global_textlist[cursor_x-1] != ' ':
                handle_one_key(keystroke, shift_mode, ctrl_mode)
        elif keystroke == "right":
            if cursor_x  < len(global_textlist):
                cursor_x += 1
            if ctrl_mode and global_textlist[cursor_x+1] != ' ':
                    handle_one_key(keystroke, shift_mode, ctrl_mode)
        elif keystroke == 'enter':
            global_textlist.insert(cursor_x, "\n")
            cursor_x += 1
        elif keystroke == 'backspace':
            global_textlist.pop(cursor_x-1)
            cursor_x -= 1
            if ctrl_mode and global_textlist[cursor_x-1] != ' ':
                handle_one_key(keystroke, shift_mode, ctrl_mode)
        else:
            global_textlist.insert(cursor_x, keystroke)
            cursor_x +=1
    except IndexError:
        pass
        
    


def handle_combo(local_keystrokes, shift_mode, ctrl_mode):
    if (dict_key := tuple(sorted(local_keystrokes))) in combo.keys():
        for keystroke in combo[dict_key]:
            handle_one_key(keystroke, shift_mode, ctrl_mode)
    else:
        for keystroke in local_keystrokes:
            handle_one_key(keystroke, shift_mode, ctrl_mode)

def update_global_textlist_and_cursor():
    # BUG shift mode with backspace
    # TODO investigate pygame.KMOD_SHIFT
    # TODO ctrl mode the cursor and backspace behaviour
    global local_keylist, global_textlist, cursor_x
    SHIFT = 1073742049
    CTRL = 1073742048
    shift_mode = False
    ctrl_mode = False
    if SHIFT in local_keylist:
        local_keylist.remove(SHIFT)
        shift_mode = True # and then move on
    if CTRL in local_keylist:
        local_keylist.remove(CTRL)
        ctrl_mode = True
    

    if shift_mode:
        local_keystrokes = [event_key_char_map_shift[key] for key in local_keylist]
    else:
        local_keystrokes = [event_key_char_map[key] for key in local_keylist]

    if set(('backspace', 'enter', 'ctrl')).intersection(set(local_keystrokes)) != set():
        for keystroke in local_keystrokes:
            handle_one_key(keystroke, shift_mode, ctrl_mode)
    else: # everykey in local_keylist is normal
        handle_combo(local_keystrokes, shift_mode, ctrl_mode)
    local_keylist = []


def get_text(event, blink_show):
    # TODO start combination keywords
    global global_textlist, cursor_x
    if get_n_key_pressed() == 0:
        update_global_textlist_and_cursor()
        
    if blink_show:
        global_text = ''.join(global_textlist[:cursor_x]+['▯']+global_textlist[cursor_x+1:])
    else:
        global_text = ''.join(global_textlist)
    return global_text
        
        

def draw_screen(event, blink_show):
    screen.fill((255, 255, 255))
    global_text = get_text(event, blink_show)
    if global_text is not None:
        draw_text(global_text)
    pygame.display.update()


if __name__ == "__main__":
    # TODO select a paragraph with shift + directional
    # TODO cursor with up down command
    clock = pygame.time.Clock()
    run = True
    i = 0
    while run:
        i+=1
        clock.tick(FPS:=60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            handle_keypress(event)
        draw_screen(event, blink_show:=(i//30)%2)            
    pygame.quit()

    

