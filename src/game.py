import argparse
import re
import sys
import time
import itertools as it
import random
from os import path

import numpy as np
import pygame
from pygame import mixer

from action import Action
from score import Score
from utils import draw_rock_meter, draw_score, draw_score_multiplier

FRET_HEIGHT = 256
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 720
# TODO: com TICKS_PER_UPDATE = 1 ta quebrando
TICKS_PER_UPDATE = 3
MS_PER_MIN = 60000

# TODO: qdo aumenta mto, da errado (ex 500)
PIXELS_PER_BEAT = 400
# PIXELS_PER_BEAT -> best offset
# 200 -> 600
# 20 -> 850

color_x_pos = [163, 227, 291, 355, 419]


class Note(pygame.sprite.Sprite):
    def __init__(self, song, imgs, start=0, note_type='N', color=None, duration=0):
        if color is None:
            raise TypeError("missing required argumet on note: color")
        elif not note_type in ('N', 'S'):
            raise TypeError("note_type must be 'N' or 'S'")

        super().__init__()
        self.start = int(start)
        self.type = 0 if note_type == 'N' else 1   # 0 = normal note, 1 = star
        self.color = int(color)
        self.duration = int(duration)

        self.__set_image(imgs, self.color)
        self.last_ticks = 0

        self.rect.x = color_x_pos[self.color]

        # note_beat = (note.start / float(song.resolution))# + song.offset
        # TODO: lembrar de levar em consideração o offset
        #print("NOTE BEAT:", note_beat)
        #pixels_per_beat = (song.bpm / 60.0) * 360
        #print("PPB:", pixels_per_beat)
        #note.y_pos = (- (note_beat * pixels_per_beat)) / song.divisor
        #print("Y:", note.y_pos)
        # TODO: Decide best way to start note's y values
        #note.y_pos = -(300 * note.start // song.resolution)
        self.y_pos = -(PIXELS_PER_BEAT * (self.start +
                                          song.offset) / song.resolution)

    def __repr__(self):
        return f'<Note start:{self.start} type:{self.type} color:{self.color} duration:{self.duration}>'

    def __str__(self):
        return f'Note: start={self.start}, type={self.type}, color={self.color}, duration={self.duration}'

    def __set_image(self, imgs, color):
        self.image = imgs[color + self.type * 5]
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

    def update(self, to_kill=None):
        self.rect.y = int(self.y_pos) + (SCREEN_HEIGHT-90)
        self.y_pos += 30

        if self.rect.y > SCREEN_HEIGHT + 60 or to_kill == True:
            self.kill()


class Song():
    def __init__(self):
        self.offset = 0
        self.resolution = 192
        self.bpm = 120  # Must be read from chart on [SyncTrack]
        self.divisor = 3
        self.name = ''
        self.guitar = ''
        self.bpm_dict = {}  # Should be a matrix
        self.ts = 4
        self.ts_dict = {}  # Should be a matrix


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "chart_file",
        help="Path to .CHART file.")
    parser.add_argument('--decrease_score', action='store_true',
                        help='enables the feature of decreasing the score for mistakes.')
    parser.add_argument('--human', action='store_true',
                        help='enables human controls through keyboard.')
    parser.add_argument('-d',
                        '--difficulty', help='choose game difficulty (Easy, Medium, Hard, Expert)')
    parser.add_argument('-s', '--screen', action='store_true',
                        help='enable the game monitoring during training.')
    parser.add_argument(
        '--config', help='file containing settings for reward and score.')
    return parser.parse_args()


def load_imgs():
    imgs = []
    img_button = []
    colors = ['green', 'red', 'yellow', 'blue', 'orange']

    for name in colors:
        sprite = pygame.image.load(
            path.join('..', 'assets', "_" + name + 'button.png')).convert_alpha()
        imgs.append(sprite)

    for name in colors:
        sprite = pygame.image.load(
            path.join('..', 'assets', name + 'button.png')).convert_alpha()
        img_button.append(sprite)

    for name in colors:
        sprite = pygame.image.load(
            path.join('..', 'assets', name + 'star.png')).convert_alpha()
        imgs.append(sprite)

    return imgs, img_button


def create_button_list(imgs, buttons_sprites_list, difficulty=5):
    buttons = []

    for i in range(difficulty):
        button = create_button(imgs[i], color_x_pos[i])
        buttons.append(button)
        buttons_sprites_list.add(button)

    return buttons


def create_button(img, x_pos):
    button = pygame.sprite.Sprite()
    button.image = pygame.transform.scale(img, (60, 60))
    button.rect = button.image.get_rect()
    button.rect.y = SCREEN_HEIGHT-90
    button.rect.x = x_pos
    return button


def load_chart(filename, imgs, difficulty=None):
    f = open(filename, 'r')
    chart_data = f.read().replace('  ', '')
    f.close()

    song = load_song_info(chart_data)
    if difficulty:
        notes = load_notes(chart_data, song, imgs, difficulty)
    else:
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
            song.offset = int(info[2]) + 0

        if (info[0] == 'Resolution'):
            song.resolution = int(info[2])

        if (info[0] == 'MusicStream'):
            song.name = info[2].strip('\"')

        if (info[0] == 'GuitarStream'):
            song.guitar = info[2]

    load_resolutions(chart_data, song)
    return song


def load_resolutions(chart_data, song):
    search_string = '[SyncTrack]\n{\n'
    inf = chart_data.find(search_string)
    sup = chart_data[inf:].find('}')
    sup += inf
    inf += len(search_string)

    resolutions_data = chart_data[inf:sup]

    for line in resolutions_data.splitlines():
        res = line.split()

        if res[2] == 'B':
            song.bpm_dict[int(res[0])] = int(res[3])/1000
        elif res[2] == 'TS':
            song.ts_dict[int(res[0])] = int(res[3])

    song.bpm = song.bpm_dict[0]
    song.ts = song.ts_dict[0]


def load_notes(chart_data, song, imgs, difficulty='EasySingle'):

    search_string = "[" + difficulty+"Single" + "]\n{\n"
    inf = chart_data.find(search_string)
    sup = chart_data[inf:].find('}')
    sup += inf
    inf += len(search_string)

    notes_data = chart_data[inf:sup]

    # pattern of the data for each note line
    #                   time    /  type / color / duration
    prog = re.compile("([0-9]+) = ([NS]) ([0-4]) ([0-9]+)")
    # time -> when the note is supposed to be played
    # type -> either normal or a star
    # color -> green, red, yellow, blue or orange.
    #           it has 0-4 so it gets only those 5 notes.
    #           If desired, can be set 0-6 to have all 7 notes in the sheet
    #           however, it requires the rest of the system to handle more
    #           note possibilities
    # duration -> allows to have any integer number as value.
    #           Could check on re docs to figure out a maximum number of characters.

    # getting all line's data parsed
    lines = prog.findall(notes_data)

    # using list comprehension to create a list of all the notes
    # and parsing the required information to the Note constructor
    #notes = [Note(song, imgs, *line) for line in lines]

    notes = []
    actions = [list(i) for i in it.product([0, 1], repeat=5)]

    for i in range(0, 1921, 48):
        a = random.choice(actions)
        for j in range(len(a)):
            if a[j]:
                notes.append(Note(song, imgs, i, 'N', j, 0))

    return notes


handle_input = Action()


def render(screen, score, buttons_sprites_list, visible_notes_list):
    # Draw Phase
    screen.fill((0, 0, 0))

    # draw guitar neck
    pygame.draw.rect(screen, (50, 50, 50), (160, 0, 320, SCREEN_HEIGHT))

    # draw neck borders
    pygame.draw.rect(screen, (200, 200, 200), (140, 0, 20, SCREEN_HEIGHT))
    pygame.draw.rect(screen, (200, 200, 200), (480, 0, 20, SCREEN_HEIGHT))

    for i in range(500):
        y_offset = (i * PIXELS_PER_BEAT)
        pygame.draw.rect(screen, (180, 180, 180),
                         (160, SCREEN_HEIGHT-y_offset-60-2, 320, 4))
        pygame.draw.rect(screen, (100, 100, 100),
                         (160, SCREEN_HEIGHT-y_offset+128-60-2, 320, 4))

    # draw Notes and Buttons
    buttons_sprites_list.draw(screen)
    visible_notes_list.draw(screen)
    # draw score
    draw_score(screen, str(score.value), score.font_size, score.x_pos)

    draw_rock_meter(score, screen, x_pos=75, y_pos=500)

    draw_score_multiplier(score, screen, x_pos=100, y_pos=600)

    pygame.display.flip()

    return screen


recent_note_history = []
# TODO: separar handle input do update


def update(score, ticks, action, song, visible_notes_list, all_notes_list, Buttons, clock, reward_value):
    global recent_note_history
    reward = 0.0
    done = False

    # Poorly updates song BPM and TS values
    if ticks in song.bpm_dict:
        song.bpm = song.bpm_dict[ticks]
    if ticks in song.ts_dict:
        song.ts = song.ts_dict[ticks]

    # Add the first 50 notes to the "visible" notes list (the ones that will be rendered)
    visible_notes_list.add(all_notes_list.sprites()[50::-1])

    # Check for collisions
    Buttons_hit_list_by_color = [
        pygame.sprite.spritecollide(
            button_type,
            visible_notes_list,
            False,
            pygame.sprite.collide_circle_ratio(0.6)
        ) for button_type in Buttons]

    # Unoptimized unpressed notes detection:
    Buttons_hit_list = []
    for button_color in Buttons_hit_list_by_color:
        Buttons_hit_list += button_color

    for note in Buttons_hit_list:
        if not note in recent_note_history:
            recent_note_history.append(note)

    for note in recent_note_history:
        if not note in Buttons_hit_list:

            done = score.miss()
            reward = -reward_value
            recent_note_history.remove(note)
    # Finished unoptimized unpressed notes detection:

    # keys = 'asdfg'  # could be a list, tuple or dict instead
    # for event in pygame.event.get():

    for n, notes_in_hit_zone in enumerate(Buttons_hit_list_by_color):
        # Eg: event.key == pygame.K_a
        # if event.key == getattr(pygame, f"K_{keys[n]}"):
        if action[n]:
            if len(notes_in_hit_zone) > 0:
                notes_in_hit_zone[0].update(True)
                recent_note_history.remove(notes_in_hit_zone[0])

                score.hit()
                reward = reward_value
            else:
                # key was pressed but without any note
                done = score.miss_click()
                reward = -reward_value

    # Move notes down
    all_notes_list.update()

    # If there are no more notes, end the game
    if len(all_notes_list) == 0:
        done = True

    clock.tick(60)

    return done, reward


def get_obs(screen, score, buttons_sprites_list, visible_notes_list):
    render(screen, score, buttons_sprites_list, visible_notes_list)
    obs = pygame.surfarray.array3d(screen).swapaxes(1, 0)
    return obs


# def step(action):
#     global done
#     reward = 0
#     done, reward = update(score, ticks, action, song,
#                           visible_notes_list, all_notes_list, Buttons, clock)
#     observation = get_obs(screen, score, buttons_sprites_list, visible_notes_list)
#     return observation, reward, done, {}


# if __name__ == "__main__":

#     difficulty_dict = {
#         "Easy":3,
#         "Medium":4,
#         "Hard":5,
#         "Expert":5
#     }

#     args = arg_parser()

#     pygame.init()
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     imgs, img_button = load_imgs()

#     song, notes = load_chart(args.chart_file, imgs, args.difficulty)

#     all_notes_list = pygame.sprite.Group()
#     buttons_sprites_list = pygame.sprite.Group()
#     visible_notes_list = pygame.sprite.Group()

#     Buttons = create_button_list(
#         img_button, buttons_sprites_list, difficulty_dict[args.difficulty])

#     for note in notes:
#         all_notes_list.add(note)
#         # buttons_sprites_list.add(note)

#     # Game Loop
#     score = Score(decrease_mode=args.decrease_score)
#     clock = pygame.time.Clock()

#     # Audio won't be used now
#     # mixer.init()
#     # audio_name = '../charts/' + song.name
#     # print("You are playing {}.".format(audio_name))
#     # song_audio = mixer.Sound(audio_name)
#     # song_audio.set_volume(0.1)
#     # song_audio.play()

#     ticks = 0
#     done = False
#     total_reward = 0
#     game_is_running = True
#     action = [False, False, False, False, False]
#     print("The Game is Running now!")

#     while game_is_running:
#         # start_time = time.time()

#         new_state, reward, done, _ = step(action)

#         total_reward += reward

#         # print(clock.get_time())
#         # print(clock.get_rawtime())
#         # print(clock.get_fps())
#         # print('Game Speed: {}'.format((num_updates) / (time.time() - start_time)))
#         # print('Render FPS: {}'.format(1.0 / (time.time() - start_time)))
#         if done:
#             game_is_running = False
#     print("Pontuação Final: {} pontos!".format(score.value))
#     print("Recompensa total do agente: {}.".format(total_reward))

#     # song_audio.stop()
#     # mixer.quit()

#     pygame.quit()
# sys.exit()
