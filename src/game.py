import argparse
import time
from os import path

import pygame
from pygame import mixer

from utils import draw_line, draw_score

FRET_HEIGHT = 256
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 720
# TODO: com TICKS_PER_UPDATE = 1 ta quebrando
TICKS_PER_UPDATE = 5
MS_PER_MIN = 60000

# TODO: qdo aumenta mto, da errado (ex 500)
PIXELS_PER_BEAT = 400
# PIXELS_PER_BEAT -> best offset
# 200 -> 600
# 20 -> 850

color_x_pos = [163, 227, 291, 355, 419]

# global_speed = 1
game_is_running = True


class Score():
    def __init__(self, decrease_mode=False):
        self.value = 0
        self.x_pos = SCREEN_WIDTH - 100
        self.font_size = 25
        self.decrease_mode = decrease_mode
        self._counter = 0

    def hit(self):
        self._counter = min(self._counter + 1, 39)
        self.value += 10 * (1 + self._counter // 10)

    def miss(self):
        self._counter = 0
        self.value -= 10 * self.decrease_mode

    @property
    def counter(self):
        return self._counter + 1
    


class Note(pygame.sprite.Sprite):
    def __init__(self, imgs, color):
        super().__init__()
        self.start = 0
        self.type = 0  # 0 = normal note, 1 = star
        self.color = color
        self.duration = 0
        self.__set_image(imgs, self.color)
        self.last_ticks = 0
        self.y_pos = 0

    def __repr__(self):
        return f'<Note start:{self.start} type:{self.type} color:{self.color} duration:{self.duration}>'

    def __str__(self):
        return f'Note: start={self.start}, type={self.type}, color={self.color}, duration={self.duration}'

    def __set_image(self, imgs, color):
        self.image = imgs[color]
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

    def update(self, to_kill=None):
        self.rect.y = int(self.y_pos) + (SCREEN_HEIGHT-90)
        self.y_pos += (TICKS_PER_UPDATE * PIXELS_PER_BEAT / song.resolution)
        
        if self.rect.y > SCREEN_HEIGHT + 60 or to_kill == True:
            self.kill()


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "chart_file",
        help="Path to .CHART file.")
    parser.add_argument('--decrease_score', action='store_true', help='enables the feature of decreasing the score for mistakes')
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
    button.rect.y = SCREEN_HEIGHT-90
    button.rect.x = x_pos
    return button


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
            song.offset = int(info[2]) + 600

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


def load_notes(chart_data, song, imgs, difficulty='ExpertSingle'):

    search_string = "[" + difficulty + "]\n{\n"
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
            # note.start = int(n[0]) - 120  # global_offset
            note.start = int(n[0])  # global_offset

            # print(note.start)

            note.duration = int(n[4])
            note.rect.x = color_x_pos[note.color]

            # note_beat = (note.start / float(song.resolution))# + song.offset
            # TODO: lembrar de levar em consideração o offset
            #print("NOTE BEAT:", note_beat)
            #pixels_per_beat = (song.bpm / 60.0) * 360
            #print("PPB:", pixels_per_beat)
            #note.y_pos = (- (note_beat * pixels_per_beat)) / song.divisor
            #print("Y:", note.y_pos)
            # TODO: Decide best way to start note's y values
            #note.y_pos = -(300 * note.start // song.resolution)
            note.y_pos = -(PIXELS_PER_BEAT * (note.start +
                                              song.offset) / song.resolution)
            #print("y: ", note.y_pos)
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

    pygame.display.flip()

    return

recent_note_history = []
# TODO: separar handle input do update
def update(score, ticks):
    global game_is_running, recent_note_history

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
            score.reset()
            recent_note_history.remove(note)
    # Finished unoptimized unpressed notes detection:

    keys = 'asdfg' #could be a list, tuple or dict instead
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_is_running = False

        if event.type == pygame.KEYDOWN:
            for n, button_in_hit_zone in enumerate(Buttons_hit_list_by_color):
                if event.key == getattr(pygame, f"K_{keys[n]}"): #Eg: event.key == pygame.K_a
                    if len(button_in_hit_zone) > 0:
                        button_in_hit_zone[0].update(True)
                        recent_note_history.remove(button_in_hit_zone[0])
                        score.add()
                    else:
                        #key was pressed but without any note
                        score.reset()

                    break
                    # exits the inner for
                    # So, those ifs work as if-elif even inside the for loop

    # Move notes down
    all_notes_list.update(ticks)

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

    Buttons = create_button_list(
        imgs, buttons_sprites_list)

    for note in notes:
        all_notes_list.add(note)
        # buttons_sprites_list.add(note)

    # Game Loop
    score = Score(decrease_mode=args.decrease_score)
    game_is_running = True
    clock = pygame.time.Clock()

    mixer.init()
    audio_name = '../charts/' + song.name
    print("You are playing {}.".format(audio_name))
    song_audio = mixer.Sound(audio_name)
    song_audio.set_volume(0.3)
    song_audio.play()
    
    ticks = 0
    update_ticks = 0
    start_ms = pygame.time.get_ticks()
    
    print("The Game is Running now!")
    
    while game_is_running:
        start_time = time.time()

        current_ms = pygame.time.get_ticks()
        delta_ms = current_ms - start_ms
        #delta_ms = clock.get_time()
        start_ms = current_ms

        # TODO: o jogo deve rodar baseado nos ticks e nao nos milissegundos
        #print("res:", song.resolution, "bpm: ", song.bpm, "ms/min:", MS_PER_MIN, "ts:",  song.ts)
        tick_per_ms = song.resolution * song.bpm / MS_PER_MIN
        delta_ticks = tick_per_ms * delta_ms
        update_ticks += delta_ticks
        
        num_updates = 0
        
        while (TICKS_PER_UPDATE <= update_ticks):
            print('--------UPDATE-------')
            print(ticks)
            update(score, ticks)
            update_ticks -= TICKS_PER_UPDATE
            num_updates += 1
            ticks += TICKS_PER_UPDATE

        handle_inputs()

        render_interval = update_ticks / TICKS_PER_UPDATE
        render(screen, render_interval, score)
        
        clock.tick(60)
        # print(clock.get_time())
        # print(clock.get_rawtime())
        # print(clock.get_fps())
        # print('Game Speed: {}'.format((num_updates) / (time.time() - start_time)))
        # print('Render FPS: {}'.format(1.0 / (time.time() - start_time)))

    print("Pontuação Final: {} pontos!".format(score.value))

    song_audio.stop()
    mixer.quit()

    pygame.quit()
