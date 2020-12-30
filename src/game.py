import argparse
import math
import random
from os import path

import pygame
from pygame import mixer

from utils import draw_line, draw_score

DEFAULT_RESOLUTION = 192

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "chart_file",
        help="Path to .CHART file.")
    return parser.parse_args()

class Note(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.start = 0
        self.type = 0 # 0 = normal note, 1 = star
        self.color = 0
        self.duration = 0
        self.image = img
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        # print(self.rect)
    def __repr__(self):
        return f'<Note start:{self.start} type:{self.type} color:{self.color} duration:{self.duration}>'
        
    def __str__(self):
        return f'Note: start={self.start}, type={self.type}, color={self.color}, duration={self.duration}'
    
    def update(self, to_kill=None):
        if self.rect.y > screen_height + 60 or to_kill == True:
            self.kill()

        self.rect.y += 1


class Button(pygame.sprite.Sprite):
    def __init__(self, img, color):
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


# GreenFret
greenImg = pygame.image.load(
    path.join('..', 'assets', 'greenbutton.png')).convert()
greenFret = Button(greenImg, 'green')
all_sprites_list.add(greenFret)

# RedFret
redImg = pygame.image.load(
    path.join('..', 'assets', 'redbutton.png')).convert()
redFret = Button(redImg, 'red')
all_sprites_list.add(redFret)

# YellowFret
yellowImg = pygame.image.load(
    path.join('..', 'assets', 'yellowbutton.png')).convert()
yellowFret = Button(yellowImg, 'yellow')
all_sprites_list.add(yellowFret)

# BlueFret
blueImg = pygame.image.load(
    path.join('..', 'assets', 'bluebutton.png')).convert()
blueFret = Button(blueImg, 'blue')
all_sprites_list.add(blueFret)

for i in range(50):
    rect_x = random.choice([200, 300, 400, 500])  # choose note color
    if rect_x == 200:
        note = Note(greenImg)
        note.rect.x = rect_x
        note.rect.y = random.uniform(-600*3, -60)
        green_notes_list.add(note)
    if rect_x == 300:
        note = Note(redImg)
        note.rect.x = rect_x
        note.rect.y = random.uniform(-600*3, -60)
        red_notes_list.add(note)
    if rect_x == 400:
        note = Note(yellowImg)
        note.rect.x = rect_x
        note.rect.y = random.uniform(-600*3, -60)
        yellow_notes_list.add(note)
    if rect_x == 500:
        note = Note(blueImg)
        note.rect.x = rect_x
        note.rect.y = random.uniform(-600*3, -60)
        blue_notes_list.add(note)

    all_notes_list.add(note)
    all_sprites_list.add(note)

# Game Loop
clock = pygame.time.Clock()
score = 0
done = False
# line_color = (128, 128, 128)
# polygon_points = [(150, 0), (600, 0), (600, screen_height), (150, screen_height)]
while not done:
    green_notes_hit_list = pygame.sprite.spritecollide(
        greenFret, green_notes_list, False, pygame.sprite.collide_circle_ratio(0.2))
    red_notes_hit_list = pygame.sprite.spritecollide(
        redFret, red_notes_list, False, pygame.sprite.collide_circle_ratio(0.2))
    yellow_notes_hit_list = pygame.sprite.spritecollide(
        yellowFret, yellow_notes_list, False, pygame.sprite.collide_circle_ratio(0.2))
    blue_notes_hit_list = pygame.sprite.spritecollide(
        blueFret, blue_notes_list, False, pygame.sprite.collide_circle_ratio(0.2))

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

    # pygame.draw.polygon(screen, line_color, polygon_points)
    draw_line(screen)
    all_sprites_list.draw(screen)
    draw_score(screen, str(score), 25)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()


if __name__ == "__main__":
    
    args = arg_parser()
    
    # read file
    f = open(args.chart_file, 'r')
    chart_data = f.read().replace('  ', '')
    f.close()
   
   # read file
    f = open(args.chart_file, 'r')
    chart_data = f.read().replace('  ', '')
    f.close()
    
    # load song info
    search_string = '[Song]\n{\n'
    inf = chart_data.find(search_string)
    sup = chart_data[inf:].find('}')
    sup += inf
    inf += len(search_string)
    
    song_data = chart_data[inf:sup]
    
    song_offset = 0
    song_resolution = DEFAULT_RESOLUTION
    song_name = ''
    song_guitar = ''

    for line in song_data.splitlines():
        info = line.split()
        
        if (info[0] == 'Offset'):
            song_offset = int(info[2])
            
        if (info[0] == 'Resolution'):
            song_resolution = int(info[2])
            
        if (info[0] == 'MusicStream'):
            song_name = info[2]
            
        if (info[0] == 'GuitarStream'):
            song_guitar = info[2]

    # load notes
    search_string = '[ExpertSingle]\n{\n'
    inf = chart_data.find(search_string)
    sup = chart_data[inf:].find('}')
    sup += inf
    inf += len(search_string)

    notes_data = chart_data[inf:sup]