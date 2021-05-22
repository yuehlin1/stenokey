import pygame
import time

from pygame.surfarray import pixels_green

pygame.font.init()
pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont("comicsans", 40)

def display_screen(text):
    screen.fill((255, 255, 255))
    rendered = font.render(text, True, (0, 0, 0))
    screen.blit(rendered, (0, 0))
    pygame.display.update()
run = True
l = []
total_text = []
total_text_str = ""
i = 0
seuil = 100000000000
seuil_mesure = []
while run:
    i+=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            try:
                l.append((chr(event.key), i))
            except ValueError:
                l.append(("NaN", i))
            # print(l)
        if event.type == pygame.KEYUP:
            if seuil == 100000000000:
                try:
                    seuil_mesure.append(i - l[-1][1])
                    if len(seuil_mesure) >= 5:
                        seuil = sum(seuil_mesure)/len(seuil_mesure)
                except :
                    pass
            try:
                distance = i - l[-1][1]
                print(l, distance)
                if distance < seuil:
                    for (key, i) in l:
                        if key == '\x08':
                            total_text.pop()
                        elif key == '\r':
                            total_text.append("\n")
                        else:
                            total_text.append(key)
                    # total_text += list(map(lambda x:x[0], l))
                    total_text_str = ''.join(total_text)
                else:
                    if l[0][0] == 'd' and l[1][0] == 'f':
                        total_text.append("def")
                        total_text_str = ''.join(total_text)
            except IndexError:
                pass
            l = []
    display_screen(total_text_str)

            
        # if event.type == pygame.KEYUP:
        #     if sum(iter(pygame.key.get_pressed())) == 0:
        #         print(chr(event.key), end='')
        # if event.type == pygame.KE
    # keys_pressed = pygame.key.get_pressed()
    # if keys_pressed[pygame.K_f] and keys_pressed[pygame.K_j]:
    #     print(":")
    # elif keys_pressed[pygame.K_f]:
    #     print("f")
    # elif keys_pressed[pygame.K_j]:
    #     print("j")
    
    

pygame.quit()