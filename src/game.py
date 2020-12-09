import math
import random
from os import path

import pygame
from pygame import mixer

from utils import draw_score


def EuclidianDistance(x1, y1, x2, y2):
    return math.sqrt((math.pow(x1-x2, 2)) + (math.pow(y1 - y2, 2)))


def Collision(noteX, noteY, ButtonX, ButtonY):
    distance = EuclidianDistance(noteX, noteY, ButtonX, ButtonY)
    if distance < 72:
        return True
    else:
        return False


class Note(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()

        self.image = img
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        # print(self.rect)

    def update(self, to_kill=None):
        if self.rect.y > screen_height + 60 or to_kill == True:
            self.kill()

        self.rect.y += 1


class Fret(pygame.sprite.Sprite):
    def __init__(self, img,color):
        super().__init__()

        self.image = img
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.y = 540
        if color.lower() == 'green':
            self.rect.x = 200
        if color.lower() == 'red':
            self.rect.x = 300
        if color.lower() == 'yellow':
            self.rect.x = 400
        if color.lower() == 'blue':
            self.rect.x = 500


pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

redImg = pygame.image.load(
    path.join('..', 'assets', 'redbutton.png')).convert()

green_notes_list = pygame.sprite.Group()
red_notes_list = pygame.sprite.Group()
yellow_notes_list = pygame.sprite.Group()
blue_notes_list = pygame.sprite.Group()
all_notes_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

for i in range(50):
    note = Note(redImg)
    rect_x = random.choice([200, 300, 400, 500])  # choose note color
    note.rect.x = rect_x
    note.rect.y = random.uniform(-600*3, -60)

    if rect_x == 200:
        green_notes_list.add(note)
    if rect_x == 300:
        red_notes_list.add(note)
    if rect_x == 400:
        yellow_notes_list.add(note)
    if rect_x == 500:
        blue_notes_list.add(note)

    all_notes_list.add(note)
    all_sprites_list.add(note)

# GreenFret
greenImg = pygame.image.load(
    path.join('..', 'assets', 'greenbutton.png')).convert()
greenFret = Fret(greenImg, 'green')
all_sprites_list.add(greenFret)

# RedFret
redImg = pygame.image.load(
    path.join('..', 'assets', 'redbutton.png')).convert()
redFret = Fret(redImg, 'red')
all_sprites_list.add(redFret)

# YellowFret
yellowImg = pygame.image.load(
    path.join('..', 'assets', 'yellowbutton.png')).convert()
yellowFret = Fret(yellowImg, 'yellow')
all_sprites_list.add(yellowFret)

# BlueFret
blueImg = pygame.image.load(
    path.join('..', 'assets', 'bluebutton.png')).convert()
blueFret = Fret(blueImg, 'blue')
all_sprites_list.add(blueFret)

# Game Loop
clock = pygame.time.Clock()
score = 0
done = False
while not done:
    green_notes_hit_list = pygame.sprite.spritecollide(
        greenFret, green_notes_list, False)
    red_notes_hit_list = pygame.sprite.spritecollide(
        redFret, red_notes_list, False)
    yellow_notes_hit_list = pygame.sprite.spritecollide(
        yellowFret, yellow_notes_list, False)
    blue_notes_hit_list = pygame.sprite.spritecollide(
        blueFret, blue_notes_list, False)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and len(green_notes_hit_list) > 0:
                green_notes_hit_list[0].update(True)
                # print('Pressed Green')
                score += 10
       
            if event.key == pygame.K_s and len(red_notes_hit_list) > 0:
                red_notes_hit_list[0].update(True)
                # print('Pressed Red')
                score += 10
       
            if event.key == pygame.K_d and len(yellow_notes_hit_list) > 0:
                yellow_notes_hit_list[0].update(True)
                # print('Pressed Yellow')
                score += 10
       
            if event.key == pygame.K_f and len(blue_notes_hit_list) > 0:
                blue_notes_hit_list[0].update(True)
                # print('Pressed Blue')
                score += 10
       
    if len(all_notes_list) == 0:
        done = True

    screen.fill((0, 0, 0))

    # Move notes down
    all_notes_list.update()

    all_sprites_list.draw(screen)
    draw_score(screen, str(score), 25)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
