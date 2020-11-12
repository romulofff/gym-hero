from pygame import draw


def draw_line(screen):
    """ Draw the lines where the notes will roll """
    height = screen.get_height()
    draw.line(screen, (100, 100, 100), (120, 0), (40, height), 3)
    draw.line(screen, (100, 100, 100), (160, 0), (120, height), 3)
    draw.line(screen, (100, 100, 100), (200, 0), (200, height), 3)
    draw.line(screen, (100, 100, 100), (240, 0), (280, height), 3)
    draw.line(screen, (100, 100, 100), (280, 0), (360, height), 3)

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
