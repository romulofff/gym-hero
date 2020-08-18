"""
Creating a Guitar Hero Clone Game
"""

import random
from ast import literal_eval

import pygame
from pygame import draw

pygame.init()
screen = pygame.display.set_mode((400, 400))
DONE = False

line_color = (128, 128, 128)
polygon_points = [(100, 0), (300, 0), (380, 310), (20, 310)]
clock = pygame.time.Clock()
x = [120, 160, 200, 240, 280]
Y = 0
radius = 10


def move_notes(old_x, old_y, new_notes):
    """Updates Y value"""
    new_x = []
    # Updating X coordinate
    if old_x[4] < 365:
        new_x.append(old_x[0] - 2)
        new_x.append(old_x[1] - 1)
        new_x.append(old_x[2])
        new_x.append(old_x[3] + 1)
        new_x.append(old_x[4] + 2)
    # Updating Y coordinate
    if old_y >= 0 and old_y < 275:
        new_y = old_y + 10
    elif old_y >= 275:
        new_y = 0
        new_x = [120, 160, 200, 240, 280]
        new_notes = True
        return new_x, new_y, new_notes
    return new_x, new_y, False

def update_radius(old_radius):
    """Updates the Circles radius"""
    if old_radius >= 5 and old_radius < 30:
        new_r = old_radius + 1
    elif old_radius == 30:
        new_r = old_radius
    else:
        return 10
    return new_r


def draw_note_target(is_pressed=False):
    """Draws the note target at the end of the track"""
    target_y = 360
    if is_pressed:
        target_outer_radius = 10
        target_inner_radius = 5

    else:
        target_outer_radius = 20
        target_inner_radius = 10

    gray = (55, 55, 55)

    # Outer (colored) Circle
    draw.circle(screen, (0, 255, 0), (100, target_y), target_outer_radius)
    draw.circle(screen, (255, 0, 0), (150, target_y), target_outer_radius)
    draw.circle(screen, (255, 255, 0), (200, target_y), target_outer_radius)
    draw.circle(screen, (0, 0, 255), (250, target_y), target_outer_radius)
    draw.circle(screen, (255, 128, 0), (300, target_y), target_outer_radius)
    # Inner Circle
    draw.circle(screen, gray, (100, target_y), target_inner_radius)
    draw.circle(screen, gray, (150, target_y), target_inner_radius)
    draw.circle(screen, gray, (200, target_y), target_inner_radius)
    draw.circle(screen, gray, (250, target_y), target_inner_radius)
    draw.circle(screen, gray, (300, target_y), target_inner_radius)

def draw_notes(should_draw):
    """ Draw notes according to list """
    if should_draw[0]:
        draw.circle(screen, (0, 255, 0), (x[0], Y), radius)
        draw.circle(screen, white, (x[0], Y), int(radius/2))

    if should_draw[1]:
        draw.circle(screen, (255, 0, 0), (x[1], Y), radius)
        draw.circle(screen, white, (x[1], Y), int(radius/2))

    if should_draw[2]:
        draw.circle(screen, (255, 255, 0), (x[2], Y), radius)
        draw.circle(screen, white, (x[2], Y), int(radius/2))

    if should_draw[3]:
        draw.circle(screen, (0, 0, 255), (x[3], Y), radius)
        draw.circle(screen, white, (x[3], Y), int(radius/2))

    if should_draw[4]:
        draw.circle(screen, (255, 128, 0), (x[4], Y), radius)
        draw.circle(screen, white, (x[4], Y), int(radius/2))



def handle_event(event_obj, pressed, score):
    """ Handles an event """
    if event_obj.type == pygame.KEYDOWN:
        # print(event_obj)
        if event_obj.key == 27:
            print("Bye!")
            quit()

        if event_obj.unicode == 'a' and pressed[0]:
            return update_score(score)
        if event_obj.unicode == 's' and pressed[1]:
            return update_score(score)
        if event_obj.unicode == 'd' and pressed[2]:
            return update_score(score)
        if event_obj.unicode == 'k' and pressed[3]:
            return update_score(score)
        if event_obj.unicode == 'l' and pressed[4]:
            return update_score(score)

    return score


def update_score(score):
    """ Increases score points by 10 """
    score += 10
    return score


font_name = pygame.font.match_font('arial')

def draw_score(score_screen, score_points, size):
    """ Draws score points on the screen """
    _x = 360
    _y = 50
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(score_points, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (_x, _y)
    score_screen.blit(text_surface, text_rect)


if __name__ == "__main__":

    white = (255, 255, 255)
    black = (0, 0, 0)
    SCORE = 0
    NEW_NOTES = False
    shouldBeDrawn = shouldBePressed = [False, False, False, False, False]

    print(shouldBePressed)

    with open('notes_chart6.txt', 'r') as f:
        line = f.read()
        print("Enter")
        if len(line) > 0:
            print('SPACE')
            line = line.split('\n')
    line.pop(-1)
    mylist = []
    for l in line:
        mylist.append(literal_eval(l))
    
    img = pygame.image.load('../chart5.png')
    img_rect = img.get_rect().size
    y = -img_rect[1] +380

    # Game Loop
    while not DONE:

        # Update Phase
        # if NEW_NOTES:
        #     for i in range(len(shouldBePressed)):
        #         shouldBePressed[i] = shouldBeDrawn[i] = bool(random.getrandbits(1))
        #     print(shouldBePressed)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                DONE = True
            else:
                SCORE = handle_event(event, shouldBePressed, SCORE)


        # Moving notes on screen
        x, Y, NEW_NOTES = move_notes(x, Y, NEW_NOTES)
        if Y > 0:
            radius = update_radius(radius)
        else:
            radius = 10


        # Drawing Phase
        screen.fill(black)
        screen.blit(img, (0, y))
        draw_score(screen, str(SCORE), 25)
        draw_note_target()

        y += 1
        pygame.display.flip()
        clock.tick(60)
