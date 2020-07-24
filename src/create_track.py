"""
Create a track to run sliding window over it
"""

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
    draw.line(screen, (100, 100, 100), (120, 0), (120, 2160), 3)
    draw.line(screen, (100, 100, 100), (160, 0), (160, 2160), 3)
    draw.line(screen, (100, 100, 100), (200, 0), (200, 2160), 3)
    draw.line(screen, (100, 100, 100), (240, 0), (240, 2160), 3)
    draw.line(screen, (100, 100, 100), (280, 0), (280, 2160), 3)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, int(1080*1.5)))
line_color = (128, 128, 128)
polygon_points = [(50, 0), (350, 0), (350, 3000), (50, 3000)]
x = [120, 160, 200, 240, 280]


draw.polygon(screen, line_color, polygon_points)  # Path for the notes
draw_line(screen)

for y in range(20, 2160, 60):
    draw.line(screen, (200, 200, 200), (50, y), (350, y), 3)

for y in range(20, int(1080*1.5), 20):
    draw.circle(screen, choose_color(), (choice(x), y), 10)

pygame.display.flip()
pygame.image.save(screen, 'chart.png')
