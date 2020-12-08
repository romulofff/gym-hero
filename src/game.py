import math
import random
from os import path

import pygame
from pygame import mixer


def EuclidianDistance(x1, y1, x2, y2):
    return math.sqrt((math.pow(x1-x2, 2)) + (math.pow(y1 - y2, 2)))


def Collision(noteX, noteY, ButtonX, ButtonY):
    distance = EuclidianDistance(noteX, noteY, ButtonX, ButtonY)
    if distance < 72:
        return True
    else:
        return False


class Note(pygame.sprite.Sprite):
    def __init__(self, img, imgX, imgY):
        super().__init__()

        self.img = img
        pygame.transform.scale(self.img, (60, 60))
        self.rect = self.img.get_rect()
        # print(self.rect)


pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# RED bites
redImg = pygame.image.load(
    path.join('..', 'assets', 'redbutton.png')).convert()
redX = 274
# redY = random.randint(-1472, -128)  # randomizes intial y-position
redY = 100  # randomizes intial y-position
redChange = random.uniform(2, 3)  # randomizes intial speed
red_note = Note(redImg, redX, redY)

note_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

for i in range(10):
    note = Note(redImg, redX, redY)
    note.rect.x = random.randrange(screen_width)
    note.rect.y = random.randrange(screen_height)

    note_list.add(note)
    all_sprites_list.add(note)

# Fret
redFret = Note(redImg, 670, 400)
all_sprites_list.add(redFret)

# Game Loop
clock = pygame.time.Clock()
score = 0
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))

    notes_hit_list = pygame.sprite.spritecollide(redFret, note_list, True)
