"""
Create a track to run sliding window over it
"""

from time import sleep
from random import choice

import pygame
from pygame import draw

def choose_color(x):
    """ Chooses a random color from the ones defined """
    if x == 100:
        green = (0, 255, 0)
        return green
    elif x == 150:
        red = (255, 0, 0)
        return red
    elif x == 200:
        yellow = (255, 255, 0)
        return yellow
    elif x == 250:
        blue = (0, 0, 255)
        return blue
    else:
        orange = (255, 128, 0)
        return orange
    # return choice([green, red, yellow, blue, orange])


def draw_line(screen):
    """ Draw the lines where the notes will roll """
    draw.line(screen, (100, 100, 100), (100, 0), (100, height+250), 3)
    draw.line(screen, (100, 100, 100), (150, 0), (150, height+250), 3)
    draw.line(screen, (100, 100, 100), (200, 0), (200, height+250), 3)
    draw.line(screen, (100, 100, 100), (250, 0), (250, height+250), 3)
    draw.line(screen, (100, 100, 100), (300, 0), (300, height+250), 3)

height = 2160*2

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, height+250))
line_color = (128, 128, 128)
polygon_points = [(50, 0), (350, 0), (350, height+500), (50, height+500)]
x = [100, 150, 200, 250, 300]


draw.polygon(screen, line_color, polygon_points)  # Path for the notes
draw_line(screen)

for y in range(20, height+250, 60):
    draw.line(screen, (200, 200, 200), (50, y), (350, y), 3)

notes = list()
for y in range(250, height, 30):
    _x = choice(x)
    draw.circle(screen, choose_color(_x), (_x, y), 10)
    notes.append([_x, y])


pygame.display.flip()
pygame.image.save(screen, '../chart6.png')
with open("notes_chart6.txt", "w") as f:
    for note in notes:
        f.write(str(note))
        # f.write('\n')
    f.close()
# sleep(60)