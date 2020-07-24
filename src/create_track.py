"""
Create a track to run sliding window over it
"""

from time import sleep
from random import choice

import pygame
from pygame import draw

def choose_color():
    """ Chooses a random color from the ones defined """
    green = (0, 255, 0)
    red = (255, 0, 0)
    yellow = (255, 255, 0)
    blue = (0, 0, 255)
    orange = (255, 128, 0)

    return choice([green, red, yellow, blue, orange])


def draw_line(screen):
    """ Draw the lines where the notes will roll """
    draw.line(screen, (100, 100, 100), (100, 0), (100, height), 3)
    draw.line(screen, (100, 100, 100), (150, 0), (150, height), 3)
    draw.line(screen, (100, 100, 100), (200, 0), (200, height), 3)
    draw.line(screen, (100, 100, 100), (250, 0), (250, height), 3)
    draw.line(screen, (100, 100, 100), (300, 0), (300, height), 3)

height = 2160*2

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, height))
line_color = (128, 128, 128)
polygon_points = [(50, 0), (350, 0), (350, height), (50, height)]
x = [100, 150, 200, 250, 300]


draw.polygon(screen, line_color, polygon_points)  # Path for the notes
draw_line(screen)

for y in range(20, height, 60):
    draw.line(screen, (200, 200, 200), (50, y), (350, y), 3)

for y in range(20, height, 20):
    draw.circle(screen, choose_color(), (choice(x), y), 10)

pygame.display.flip()
pygame.image.save(screen, '../chart.png')
# sleep(60)