import os
import argparse

import numpy as np
import pygame
from pygame import draw


parser = argparse.ArgumentParser(description="Run GuitarHero PyGame")
parser.add_argument('--screen_render', default=1, type=int, help="Pass 1 or 0 to turn on or off Screen Rendering")
parser.add_argument('--resolution', default=(680,480), nargs='+', help="width height ")

args = parser.parse_args()
print(type(args.resolution))
print(args.resolution)
if not bool(args.screen_render):
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.environ["SDL_VIDEODRIVER"] = "dummy"

pygame.init()
res = (int(args.resolution[0]), int(args.resolution[1]))
print(res)
screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()

count = 0
x = 0
y = 10
start_ticks=pygame.time.get_ticks()
while True:
    x += 2
    if x >= res[0]:
        x = 0
        y +=10
    if y >= res[1]: break
    
    screen.fill((0,0,0))
    draw.circle(screen, (255,0,0), (x,y), 10)
    draw.circle(screen, (255,0,0), (res[0]-x,res[1]-y), 10)

    pygame.display.flip()
    count += 1
    seconds=(pygame.time.get_ticks()-start_ticks)/1000

    print(seconds)
    # clock.tick(30)
    if seconds >= 1:
        print(count)
        count = 0
        break
    