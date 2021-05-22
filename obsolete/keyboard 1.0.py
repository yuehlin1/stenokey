# In this file, a notepad-like environment is coded with pygame. You can
# - type words using english keyboard (at the position of cursor)
# - shift + word becomes uppercase
# - capslock has no effect
# - enter, backspace work (at the position of cursor)
# - cursor only supports left and right, up and down has no effect
# - TODO combo keys to be implemented
#   - TODO recreate local_keylist so that it takes in time argument as well
#     so that we can distinguish combo keys from typing too fast
#   - TODO update_global_textlist_and_cursor needs to be revisited. It shouldn't
#     visiting every key in local_keylist at a time, rather look at the whole list

import pygame
pygame.init()
pygame.font.init()


screen = pygame.display.set_mode((500, 500))
event_number = [96, 49, 50, 51, 52, 53, 54, 55, 
                56, 57, 48, 45, 61, 113, 119, 101, 
                114, 116, 121, 117, 105, 111, 112, 
                91, 93, 97, 115, 100, 102, 103, 104, 
                106, 107, 108, 59, 39, 92, 122, 120, 
                99, 118, 98, 110, 109, 44, 46, 47, 32]
event_key_char_map = dict(zip(event_number, list("`1234567890-=qwertyuiop[]asdfghjkl;'\zxcvbnm,./ ")))
event_key_char_map_shift = dict(zip(event_number, list('~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>? ')))
event_key_char_map[1073742049] = 'shift'
event_key_char_map[8] = 'backspace'
event_key_char_map[13] = 'enter'
event_key_char_map[1073742048] = 'ctrl'


local_keylist = []
global_textlist = []
font = pygame.font.SysFont("arial", 40)
cursor_x = 0 # it should be between 0 and len(global_textlist)


def get_n_key_pressed():
    return sum(iter(pygame.key.get_pressed()))

def handle_keydown(event):
    global cursor_x
    if event.key == pygame.K_LEFT:
        cursor_x -= 1
    elif event.key == pygame.K_RIGHT:
        if cursor_x  < len(global_textlist):
            cursor_x += 1
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

def update_global_textlist_and_cursor():
    # TODO refactor this to use less if conditon
    global local_keylist, global_textlist, cursor_x
    shift_mode = False
    for key in local_keylist:
        keystroke = event_key_char_map_shift[key] if shift_mode else event_key_char_map[key]
        if keystroke == 'enter':
            global_textlist.insert(cursor_x, "\n")
            cursor_x += 1
        elif keystroke == 'backspace':
            try:
                global_textlist.pop(cursor_x-1)
                cursor_x -= 1
            except IndexError:
                pass
        elif keystroke == "shift":
            shift_mode = True
        else:
            global_textlist.insert(cursor_x, keystroke)
            cursor_x +=1
    local_keylist = []


def get_text(blink_show):
    # TODO start combination keywords
    global local_keylist, global_textlist, cursor_x
    if get_n_key_pressed() == 0:
        update_global_textlist_and_cursor()
        
    if blink_show:
        global_text = ''.join(global_textlist[:cursor_x]+['▯']+global_textlist[cursor_x+1:])
    else:
        global_text = ''.join(global_textlist)
    return global_text
        
        

def draw_screen(blink_show):
    screen.fill((255, 255, 255))
    global_text = get_text(blink_show)
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
        draw_screen(blink_show:=(i//30)%2)            
    pygame.quit()

