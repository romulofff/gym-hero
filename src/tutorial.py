# Tutorial from Reddit
# https://www.reddit.com/r/pygame/comments/9z4kpq/how_to_create_a_rhythm_game/

import random
from time import time

import pygame
from numpy import arange

pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffersize=512)
pygame.init()

screen = pygame.display.set_mode((480, 360))

when_things_happen = [x for x in arange(0, 10, 0.5)]
print(when_things_happen, len(when_things_happen))
start_time = time()


if __name__ == "__main__":
    running = True
    while running:
        elapsed_time = time() - start_time
        happening = [x for x in when_things_happen if x <= elapsed_time]
        print(happening)
        for x in happening:
            when_things_happen.remove(x)