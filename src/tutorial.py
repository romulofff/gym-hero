# Tutorial from Reddit
# https://www.reddit.com/r/pygame/comments/9z4kpq/how_to_create_a_rhythm_game/

import random
from time import time

import pygame
from pygame import draw
from numpy import arange

# pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffersize=512)
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((400, 720))

when_things_happen = [x for x in arange(0, 10, 0.5)]
# print(when_things_happen, len(when_things_happen))
start_time = time()

interval = 10.0
def check_if_close(elapsed_time, times):
    for time in times:
        if elapsed_time - interval <= time <= elapsed_time + interval:
        # if time - interval <= elapsed_time <= time + interval:
        
           print(elapsed_time, time+interval, time-interval, time)
           return True
        print(elapsed_time, time+interval, time-interval, time)

    return False

def draw_note_target():
    """Draws the note target at the end of the track"""
    target_y = 660
    target_outer_radius = 30
    target_inner_radius = 15

    gray = (55, 55, 55)

    # Outer (colored) Circle
    draw.circle(screen, (0, 255, 0), (64, target_y), target_outer_radius)
    draw.circle(screen, (255, 0, 0), (132, target_y), target_outer_radius)
    draw.circle(screen, (255, 255, 0), (200, target_y), target_outer_radius)
    draw.circle(screen, (0, 0, 255), (268, target_y), target_outer_radius)
    draw.circle(screen, (255, 128, 0), (336, target_y), target_outer_radius)
    # Inner Circle
    draw.circle(screen, gray, (64, target_y), target_inner_radius)
    draw.circle(screen, gray, (132, target_y), target_inner_radius)
    draw.circle(screen, gray, (200, target_y), target_inner_radius)
    draw.circle(screen, gray, (268, target_y), target_inner_radius)
    draw.circle(screen, gray, (336, target_y), target_inner_radius)

if __name__ == "__main__":
    running = True
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, 50)
    while running:
        color = (255,255,255)
        if len(when_things_happen) == 0: running = False
        elapsed_time = time() - start_time
        happening = [x for x in when_things_happen if x <= elapsed_time]
        print(happening)

        for e in pygame.event.get():
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
            screen.blit(text_surface, (180,140))
            when_things_happen.remove(x)
        draw_note_target()
        pygame.display.update()
        clock.tick(10)