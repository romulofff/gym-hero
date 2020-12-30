import argparse
from os import path

import pygame
from pygame import mixer

from utils import draw_line, draw_score

DEFAULT_RESOLUTION = 192
FRET_HEIGHT = 256
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 900

color_x_pos = [192, 256, 320, 384, 448]


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "chart_file",
        help="Path to .CHART file.")
    return parser.parse_args()


def load_imgs():
    greenImg = pygame.image.load(
        path.join('..', 'assets', 'greenbutton.png')).convert()

    redImg = pygame.image.load(
        path.join('..', 'assets', 'redbutton.png')).convert()

    yellowImg = pygame.image.load(
        path.join('..', 'assets', 'yellowbutton.png')).convert()

    blueImg = pygame.image.load(
        path.join('..', 'assets', 'bluebutton.png')).convert()

    imgs = [greenImg, redImg, yellowImg, blueImg]
    return imgs


class Note(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.start = 0
        self.type = 0  # 0 = normal note, 1 = star
        self.color = 0
        self.duration = 0
        self.__set_image(self.color)

    def __repr__(self):
        return f'<Note start:{self.start} type:{self.type} color:{self.color} duration:{self.duration}>'

    def __str__(self):
        return f'Note: start={self.start}, type={self.type}, color={self.color}, duration={self.duration}'

    def __set_image(self, img):
        self.image = imgs[img]
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        # print(self.rect)

    def update_color(self, color):
        self.color = color
        # print(self.color)
        self.__set_image(self.color)

    def update(self, to_kill=None):
        """
        TODO: Precisa ser modificada para atualizar a posição y
            com base na resolução da música. 

            y = (256 * note.start // song_resolution) + global_y_offset

            global_offset tem que ser atualizado também (ele que move as notas)
        """
        if self.rect.y > SCREEN_HEIGHT + 60 or to_kill == True:
            self.kill()

        self.rect.y += (256 * self.start // song_resolution) + global_y_offset


def create_buttons(imgs):
    greenButton = Button(imgs[0], 'green')
    redButton = Button(imgs[1], 'red')
    yellowButton = Button(imgs[2], 'yellow')
    blueButton = Button(imgs[3], 'blue')
    all_sprites_list.add(greenButton)
    all_sprites_list.add(redButton)
    all_sprites_list.add(yellowButton)
    all_sprites_list.add(blueButton)
    return greenButton, redButton, yellowButton, blueButton


class Button(pygame.sprite.Sprite):
    def __init__(self, img, color):
        super().__init__()

        self.image = img
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT-0-60
        if color.lower() == 'green':
            self.rect.x = 192
        if color.lower() == 'red':
            self.rect.x = 256
        if color.lower() == 'yellow':
            self.rect.x = 320
        if color.lower() == 'blue':
            self.rect.x = 384


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
    notes = []
    stars = []

    imgs = load_imgs()
    green_notes_list = pygame.sprite.Group()
    red_notes_list = pygame.sprite.Group()
    yellow_notes_list = pygame.sprite.Group()
    blue_notes_list = pygame.sprite.Group()
    all_notes_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()
    greenButton, redButton, yellowButton, blueButton = create_buttons(imgs)

    for line in notes_data.splitlines():
        n = line.split()

        if (n[2] == 'N'):
            if (int(n[3]) > 3):
                continue
            note = Note()
            note.start = int(n[0])
            # note.color = int(n[3])
            note.duration = int(n[4])
            note.update_color(int(n[3]))
            note.rect.x = color_x_pos[note.color]
            notes.append(note)
            all_notes_list.add(note)
            all_sprites_list.add(note)

        if (n[2] == 'S'):
            stars.append(int(n[0]))
            stars.append(int(n[0])+int(n[4]))

    # set stars
    s = 0

    for i in range(len(notes)):
        if (s >= len(stars)):
            break

        if (notes[i].start >= stars[s]):
            if (notes[i].start <= stars[s+1]):
                notes[i].type = 1
            else:
                s += 2
                i -= 1

    # Game Loop
    score = 0
    running = True
    clock = pygame.time.Clock()
    global_y_offset = 0

    while running:
        # Check for collisions
        green_notes_hit_list = pygame.sprite.spritecollide(
            greenButton, green_notes_list, False, pygame.sprite.collide_circle_ratio(0.2))
        red_notes_hit_list = pygame.sprite.spritecollide(
            redButton, red_notes_list, False, pygame.sprite.collide_circle_ratio(0.2))
        yellow_notes_hit_list = pygame.sprite.spritecollide(
            yellowButton, yellow_notes_list, False, pygame.sprite.collide_circle_ratio(0.2))
        blue_notes_hit_list = pygame.sprite.spritecollide(
            blueButton, blue_notes_list, False, pygame.sprite.collide_circle_ratio(0.2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and len(green_notes_hit_list) > 0:
                    green_notes_hit_list[0].update(True)
                    print('Pressed Green')
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

        # Move notes down
        # global_y_offset += .01
        all_notes_list.update()

        # # If there are no more notes, end the game
        # if len(all_notes_list) == 0:
        #     running = False

        # Draw Phase
        screen.fill((0, 0, 0))

        # draw guitar neck
        pygame.draw.rect(screen, (50, 50, 50), (160, 0, 320, SCREEN_HEIGHT))

        # draw neck borders
        pygame.draw.rect(screen, (200, 200, 200), (140, 0, 20, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (200, 200, 200), (480, 0, 20, SCREEN_HEIGHT))

        for i in range(500):
            y_offset = (i * 256) + global_y_offset
            pygame.draw.rect(screen, (180, 180, 180),
                             (160, SCREEN_HEIGHT-y_offset-30-2, 320, 4))
            pygame.draw.rect(screen, (100, 100, 100),
                             (160, SCREEN_HEIGHT-y_offset+128-30-2, 320, 4))

        # draw Notes and Buttons
        all_sprites_list.draw(screen)

        # draw score
        draw_score(screen, str(score), 25, SCREEN_WIDTH)

        clock.tick(60)
        pygame.display.flip()
