import pygame
from pygame import draw


def handle_inputs():
    keys = 'asdfg'  # could be a list, tuple or dict instead
    actions = [False, False, False, False, False]
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            for n, key in enumerate(keys):
                if event.key == getattr(pygame, f"K_{key}"):
                    actions[n] = True

    if any(actions):
        print(actions)

    return actions


def draw_line(screen):
    """ Draw the lines where the notes will roll """
    height = screen.get_height()
    draw.line(screen, (100, 100, 100), (230, 0), (230, height), 3)
    draw.line(screen, (100, 100, 100), (330, 0), (330, height), 3)
    draw.line(screen, (100, 100, 100), (430, 0), (430, height), 3)
    draw.line(screen, (100, 100, 100), (530, 0), (530, height), 3)
    # draw.line(screen, (100, 100, 100), (0, 0), (360, height), 3)


def draw_note_target(screen):
    """Draws the note target at the end of the track"""
    height = screen.get_height()
    target_y = int(height - 10/100*height)
    target_outer_radius = 30
    target_inner_radius = 15

    gray = (55, 55, 55)

    # Outer (colored) Circle
    draw.circle(screen, (0, 255, 0), (50, target_y), target_outer_radius)
    draw.circle(screen, (255, 0, 0), (125, target_y), target_outer_radius)
    draw.circle(screen, (255, 255, 0), (200, target_y), target_outer_radius)
    draw.circle(screen, (0, 0, 255), (275, target_y), target_outer_radius)
    draw.circle(screen, (255, 128, 0), (350, target_y), target_outer_radius)
    # Inner Circle
    draw.circle(screen, gray, (50, target_y), target_inner_radius)
    draw.circle(screen, gray, (125, target_y), target_inner_radius)
    draw.circle(screen, gray, (200, target_y), target_inner_radius)
    draw.circle(screen, gray, (275, target_y), target_inner_radius)
    draw.circle(screen, gray, (350, target_y), target_inner_radius)


font_name = pygame.font.match_font('arial')
white = (255, 255, 255)


def draw_score(score_screen, score_points, size, x_position):
    """ Draws score points on the screen """
    _x = x_position
    _y = 570
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(score_points, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (_x, _y)
    score_screen.blit(text_surface, text_rect)


def draw_score_multiplier(score, surface, x_pos=0, y_pos=0, size=25):
    # code slightly modified from draw score
    font = pygame.font.Font(
        pygame.font.match_font('arial'), size)

    value = score.multiplier
    color = ((255, 255, 255),  # white for x1
             (255, 255, 0),  # yellow for x2
             (0, 255, 0),  # green for x3
             (200, 0, 200)  # purple for x4
             )[value - 1]

    multiplier = font.render(f"x{value}", True, color)

    multiplier_rect = multiplier.get_rect()
    multiplier_rect.midtop = (x_pos, y_pos)
    surface.blit(multiplier, multiplier_rect)


def draw_rock_meter(score, surface, x_pos=0, y_pos=0):
    height = 10
    width = 20

    # draws the first layer of the meeter,
    # which consists of the 3 colors, but darkened
    for i in range(3):
        pygame.draw.rect(
            surface,
            (200 * (i < 2), 180 * (i > 0), 0),
            (x_pos + i*width, y_pos, width, height)
        )

    # highlits the color the meeter is in, as if it light up
    lightned_bar = int((score.rock_meter-1) * (3 / 100))
    pygame.draw.rect(
        surface,
        (255 * (lightned_bar < 2), 255 * (lightned_bar > 0), 0),
        (x_pos + lightned_bar*width, y_pos, width, height)
    )

    # locating the position on which the bar will be:
    total_size = width * 3
    place = x_pos + (score.rock_meter / 100) * total_size

    # drawing the bar on top of meeter
    pygame.draw.line(
        surface,
        color=(255, 255, 255),
        start_pos=(place, y_pos - 5),
        end_pos=(place, y_pos + height + 5),
        width=3
    )
