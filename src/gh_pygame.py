"""
Creating a Guitar Hero Clone Game
"""
from pygame import draw
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 310))
DONE = False

line_color = (128, 128, 128)
polygon_points = [(100, 0), (300, 0), (380, 310), (20, 310)]
clock = pygame.time.Clock()
x = [120, 160, 200, 240, 280]
Y = 0
radius = 10


def move_notes(old_x, old_y):
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
    return new_x, new_y


def update_radius(old_radius):
    """Updates the Circles radius"""
    if old_radius >= 5 and old_radius < 30:
        new_r = old_radius + 1
    elif old_radius == 30:
        new_r = old_radius
    else:
        return 10
    return new_r


def draw_note_target():
    """Draws the note target at the end of the track"""
    # Outer (colored) Circle
    draw.circle(screen, (0, 255, 0), (64, 260), 30)
    draw.circle(screen, (255, 0, 0), (132, 260), 30)
    draw.circle(screen, (255, 255, 0), (200, 260), 30)
    draw.circle(screen, (0, 0, 255), (268, 260), 30)
    draw.circle(screen, (255, 128, 0), (336, 260), 30)
    # Inner Circle
    draw.circle(screen, (55, 55, 55), (64, 260), 15)
    draw.circle(screen, (55, 55, 55), (132, 260), 15)
    draw.circle(screen, (55, 55, 55), (200, 260), 15)
    draw.circle(screen, (55, 55, 55), (268, 260), 15)
    draw.circle(screen, (55, 55, 55), (336, 260), 15)


def handle_event(event_obj, score):
    """ Handles an event """
    if event_obj.type == pygame.KEYDOWN:
        # print(event_obj)
        if event_obj.key == 27:
            quit()

        if event_obj.unicode == 'a':
            return update_score(score)
    return score

def update_score(score):
    """ Increases score points by 10 """
    print("Pontuação antes: {}".format(score))
    score += 10
    print("Pontuação depois: {}".format(score))
    return score


font_name = pygame.font.match_font('arial')
def draw_score(screen, score_points, size):
    """ Draws score points on the screen """
    _x = 360
    _y = 50
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(score_points, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (_x, _y)
    screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    white = (255, 255, 255)

    SCORE = 0

    # Game Loop
    while not DONE:
        for event in pygame.event.get():

            SCORE = handle_event(event, SCORE)
            if event.type == pygame.QUIT:
                DONE = True

        screen.fill((0, 0, 0))

        draw.polygon(screen, line_color, polygon_points)  # Path for the notes
        draw_score(screen, str(SCORE), 25)
        draw_note_target()
        # Outer (colored) Circle
        draw.circle(screen, (0, 255, 0), (x[0], Y), radius)
        draw.circle(screen, (255, 0, 0), (x[1], Y), radius)
        draw.circle(screen, (255, 255, 0), (x[2], Y), radius)
        draw.circle(screen, (0, 0, 255), (x[3], Y), radius)
        draw.circle(screen, (255, 128, 0), (x[4], Y), radius)
        # Inner Circle
        draw.circle(screen, white, (x[0], Y), int(radius/2))
        draw.circle(screen, white, (x[1], Y), int(radius/2))
        draw.circle(screen, white, (x[2], Y), int(radius/2))
        draw.circle(screen, white, (x[3], Y), int(radius/2))
        draw.circle(screen, white, (x[4], Y), int(radius/2))
        x, Y = move_notes(x, Y)
        if Y > 0:
            radius = update_radius(radius)
        else:
            radius = 10

        # get_key()
        pygame.display.flip()
        clock.tick(30)
