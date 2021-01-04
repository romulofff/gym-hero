import argparse
import time
from os import path

import pygame
from pygame import mixer

from utils import draw_line, draw_score

FRET_HEIGHT = 256
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 900
MS_PER_UPDATE = 5
MS_PER_MIN = 60000

color_x_pos = [163, 227, 291, 355, 419]

global_speed = 1
game_is_running = True


class Score():
    def __init__(self):
        self.value = 0
        self.x_pos = SCREEN_WIDTH - 100
        self.font_size = 25


class Note(pygame.sprite.Sprite):
    def __init__(self, imgs, color):
        super().__init__()
        self.start = 0
        self.type = 0  # 0 = normal note, 1 = star
        self.color = color
        self.duration = 0
        self.__set_image(imgs, self.color)

    def __repr__(self):
        return f'<Note start:{self.start} type:{self.type} color:{self.color} duration:{self.duration}>'

    def __str__(self):
        return f'Note: start={self.start}, type={self.type}, color={self.color}, duration={self.duration}'

    def __set_image(self, imgs, color):
        self.image = imgs[color]
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

    def update(self, to_kill=None):
        if self.rect.y > SCREEN_HEIGHT + 60 or to_kill == True:
            self.kill()

        global global_speed
        self.rect.y += global_speed


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "chart_file",
        help="Path to .CHART file.")
    return parser.parse_args()


def load_imgs():
    imgs = []

    for name in ['green', 'red', 'yellow', 'blue', 'orange']:
        sprite = pygame.image.load(
            path.join('..', 'assets', name + 'button.png')).convert_alpha()
        imgs.append(sprite)

    return imgs


def create_button_list(imgs, buttons_sprites_list):
    buttons = []

    for i in range(5):
        button = create_button(imgs[i], color_x_pos[i])
        buttons.append(button)
        buttons_sprites_list.add(button)

    return buttons


def create_button(img, x_pos):
    button = pygame.sprite.Sprite()
    button.image = pygame.transform.scale(img, (60, 60))
    button.rect = button.image.get_rect()
    button.rect.y = SCREEN_HEIGHT-60
    button.rect.x = x_pos
    return button


class Song():
    def __init__(self):
        self.offset = 0
        self.resolution = 192
        self.name = ''
        self.guitar = ''


def load_chart(filename, imgs):

    f = open(filename, 'r')
    chart_data = f.read().replace('  ', '')
    f.close()

    song = load_song_info(chart_data)
    notes = load_notes(chart_data, song, imgs)

    return song, notes


def load_song_info(chart_data):

    search_string = '[Song]\n{\n'
    inf = chart_data.find(search_string)
    sup = chart_data[inf:].find('}')
    sup += inf
    inf += len(search_string)

    song_data = chart_data[inf:sup]

    song = Song()

    for line in song_data.splitlines():
        info = line.split()

        if (info[0] == 'Offset'):
            song.offset = int(info[2])

        if (info[0] == 'Resolution'):
            song.resolution = int(info[2])

        if (info[0] == 'MusicStream'):
            song.name = info[2]

        if (info[0] == 'GuitarStream'):
            song.guitar = info[2]

    return song


def load_notes(chart_data, song, imgs):

    search_string = '[ExpertSingle]\n{\n'
    inf = chart_data.find(search_string)
    sup = chart_data[inf:].find('}')
    sup += inf
    inf += len(search_string)

    notes_data = chart_data[inf:sup]

    notes = []
    stars = []

    for line in notes_data.splitlines():
        n = line.split()

        # TODO: checar todos os intervalos validos
        # ex: color (n[3] >= 0 e < 5)
        if (n[2] == 'N') and (int(n[3]) < 5):
            note = Note(imgs, int(n[3]))
            note.start = int(n[0]) - 120  # global_offset
            note.duration = int(n[4])
            note.rect.x = color_x_pos[note.color]
            # TODO: checar se eh msm 240
            note.rect.y = -(240 * note.start // song.resolution)
            notes.append(note)

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

    return notes


def handle_inputs():
    return


def render(screen, render_interval, score):
    # Draw Phase
    screen.fill((0, 0, 0))

    # draw guitar neck
    pygame.draw.rect(screen, (50, 50, 50), (160, 0, 320, SCREEN_HEIGHT))

    # draw neck borders
    pygame.draw.rect(screen, (200, 200, 200), (140, 0, 20, SCREEN_HEIGHT))
    pygame.draw.rect(screen, (200, 200, 200), (480, 0, 20, SCREEN_HEIGHT))

    for i in range(500):
        y_offset = (i * 256)
        pygame.draw.rect(screen, (180, 180, 180),
                         (160, SCREEN_HEIGHT-y_offset-30-2, 320, 4))
        pygame.draw.rect(screen, (100, 100, 100),
                         (160, SCREEN_HEIGHT-y_offset+128-30-2, 320, 4))

    # draw Notes and Buttons
    buttons_sprites_list.draw(screen)
    visible_notes_list.draw(screen)
    # draw score
    draw_score(screen, str(score.value), score.font_size, score.x_pos)

    pygame.display.flip()

    return


# TODO: separar handle input do update
def update(score):
    global game_is_running

    # Add the first 50 notes to the "visible" notes list (the ones that will be rendered)
    visible_notes_list.add(all_notes_list.sprites()[:50])

    # Check for collisions
    green_notes_hit_list = pygame.sprite.spritecollide(
        greenButton, visible_notes_list, False, pygame.sprite.collide_circle_ratio(0.5))
    red_notes_hit_list = pygame.sprite.spritecollide(
        redButton, visible_notes_list, False, pygame.sprite.collide_circle_ratio(0.5))
    yellow_notes_hit_list = pygame.sprite.spritecollide(
        yellowButton, visible_notes_list, False, pygame.sprite.collide_circle_ratio(0.5))
    blue_notes_hit_list = pygame.sprite.spritecollide(
        blueButton, visible_notes_list, False, pygame.sprite.collide_circle_ratio(0.5))
    orange_notes_hit_list = pygame.sprite.spritecollide(
        orangeButton, visible_notes_list, False, pygame.sprite.collide_circle_ratio(0.5))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_is_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and len(green_notes_hit_list) > 0:
                green_notes_hit_list[0].update(True)
                # print('Pressed Green')
                score.value += 10

            if event.key == pygame.K_s and len(red_notes_hit_list) > 0:
                red_notes_hit_list[0].update(True)
                # print('Pressed Red')
                score.value += 10

            if event.key == pygame.K_d and len(yellow_notes_hit_list) > 0:
                yellow_notes_hit_list[0].update(True)
                # print('Pressed Yellow')
                score.value += 10

            if event.key == pygame.K_f and len(blue_notes_hit_list) > 0:
                blue_notes_hit_list[0].update(True)
                # print('Pressed Blue')
                score.value += 10

            if event.key == pygame.K_g and len(orange_notes_hit_list) > 0:
                orange_notes_hit_list[0].update(True)
                # print('Pressed Orange')
                score.value += 10

    # Move notes down
    all_notes_list.update()

    # If there are no more notes, end the game
    if len(all_notes_list) == 0:
        game_is_running = False


if __name__ == "__main__":

    args = arg_parser()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    imgs = load_imgs()

    song, notes = load_chart(args.chart_file, imgs)

    all_notes_list = pygame.sprite.Group()
    buttons_sprites_list = pygame.sprite.Group()
    visible_notes_list = pygame.sprite.Group()

    greenButton, redButton, yellowButton, blueButton, orangeButton = create_button_list(
        imgs, buttons_sprites_list)

    for note in notes:
        all_notes_list.add(note)
        # buttons_sprites_list.add(note)

    # Game Loop
    score = Score()
    game_is_running = True
    clock = pygame.time.Clock()

    update_ms = 0
    start_ms = pygame.time.get_ticks()

    print("The Game is Running now!")
    while game_is_running:
        start_time = time.time()

        current_ms = pygame.time.get_ticks()
        delta_ms = current_ms - start_ms
        start_ms = current_ms
        update_ms += delta_ms

        # TODO: o jogo deve rodar baseado nos ticks e nao nos milissegundos
        #tick_per_ms = song.resolution * current_bpm / MS_PER_MIN
        #ticks += (ticks_per_ms * delta_ms)

        num_updates = 0

        while (MS_PER_UPDATE <= update_ms):
            update(score)
            update_ms -= MS_PER_UPDATE
            num_updates += 1

        handle_inputs()

        render_interval = update_ms / MS_PER_UPDATE
        render(screen, render_interval, score)

        clock.tick(60)
        # print(clock.get_fps())
        # print('Game Speed: {}'.format((num_updates) / (time.time() - start_time)))
        print('Render FPS: {}'.format(1.0 / (time.time() - start_time)))

    print("Pontuação Final: {} pontos!".format(score.value))
    pygame.quit()
