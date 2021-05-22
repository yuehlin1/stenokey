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
event_key_char_map_shift[8] = 'backspace'
event_key_char_map[13] = 'enter'
event_key_char_map_shift[13] = 'enter'
event_key_char_map[1073742048] = 'ctrl'
event_key_char_map_shift[1073742048] = 'ctrl'
event_key_char_map[9] = '    '

event_key_char_map[1073741904] = 'left'
event_key_char_map[1073741903] = 'right'
event_key_char_map[1073741906] = 'up'
event_key_char_map[1073741905] = 'down'