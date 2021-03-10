import pygame
from pygame import draw


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
    _y = 500
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(score_points, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (_x, _y)
    score_screen.blit(text_surface, text_rect)
