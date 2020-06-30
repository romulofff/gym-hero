"""
Creating a Guitar Hero Game
"""
from pygame import draw
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
DONE = False

line_color = (255, 255, 255)

clock = pygame.time.Clock()

while not DONE:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DONE = True

    screen.fill((0, 0, 0))

    draw.circle(screen, (0, 255, 0), (160, 50), 5)
    draw.circle(screen, (255, 0, 0), (180, 50), 5)
    draw.circle(screen, (255, 255, 0), (200, 50), 5)
    draw.circle(screen, (0, 0, 255), (220, 50), 5)
    draw.circle(screen, (255, 128, 0), (240, 50), 5)

    draw.line(screen, line_color, (150, 50), (50, 250))
    draw.line(screen, line_color, (250, 50), (350, 250))
    pygame.display.flip()
    clock.tick(60)
