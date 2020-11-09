# Tutorial from Reddit
# https://www.reddit.com/r/pygame/comments/9z4kpq/how_to_create_a_rhythm_game/
import os 
import random
from time import time

import pygame
from numpy import arange
from pygame import draw

from utils import draw_line, draw_note_target

# pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffersize=512)
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((450, 720))

when_things_happen = [x for x in arange(0, 10, 0.5)]
# print(when_things_happen, len(when_things_happen))
start_time = time()

interval = 1.0
def check_if_close(elapsed_time, times):
    for time in times:
        if elapsed_time - interval <= time <= elapsed_time + interval:
        # if time - interval <= elapsed_time <= time + interval:
        
           print(elapsed_time, time+interval, time-interval, time, True)
           return True
        print(elapsed_time, time+interval, time-interval, time)

    return False

if __name__ == "__main__":

    # NÃO VAI FUNCIONAR COM ESSA IMAGEM
    green_note = pygame.image.load(os.path.join('..', 'green_note.png')).convert()


    running = True
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, 50)
    y = 0
    while running:
        color = (255,255,255)
        if len(when_things_happen) == 0: running = False
        elapsed_time = time() - start_time
        happening = [x for x in when_things_happen if x <= elapsed_time]
        # print(happening)

        for e in pygame.event.get():
            print("Got event!", e)
            if e.type==pygame.KEYDOWN and e.key == 27:
                print("Bye!")
                quit()
            if e.type==pygame.KEYDOWN and e.key == pygame.K_SPACE:
            # if e.type==pygame.KEYDOWN:
                if check_if_close(elapsed_time, happening):
                    print("SPACE BAR PRESSED RIGHT")
                    color = (255,0,0)
                else: color = (255,255,255)

        for x in happening:
            screen.fill(0)
            text_surface = font.render(str(x), True, color)
            screen.blit(text_surface, (380,140))
            when_things_happen.remove(x)
        draw_line(screen)
        draw_note_target(screen)
        pygame.display.update()
        clock.tick(60)
