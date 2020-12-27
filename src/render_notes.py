import pygame
import argparse


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "chart_file",
        help="Path to .CHART file.")
    return parser.parse_args()


DEFAULT_RESOLUTION = 192
FRET_HEIGHT = 256
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 900

color_x_pos = [192, 256, 320, 384, 448]

color_off = [(14, 38, 10), (64, 8, 8), (94, 94, 13), (16, 24, 82), (108, 62, 0)]
color_on = [(24, 130, 12), (172, 0, 0), (224, 220, 8), (32, 48, 180), (224, 128, 0)]

white_on = (255, 255, 255)
white_off = (150, 150, 150)

black = (0, 0, 0)


class Note:
    def __init__(self):
        self.start = 0
        self.type = 0 # 0 = normal note, 1 = star
        self.color = 0
        self.duration = 0
        
    def __repr__(self):
        return f'<Note start:{self.start} type:{self.type} color:{self.color} duration:{self.duration}>'
        
    def __str__(self):
        return f'Note: start={self.start}, type={self.type}, color={self.color}, duration={self.duration}'
        

def draw_note_on(screen, color, position):
    pygame.draw.circle(screen, white_on, position, 30)
    pygame.draw.circle(screen, color, position, 28)
    pygame.draw.circle(screen, black, position, 14)
    pygame.draw.circle(screen, white_on, position, 11)
    
def draw_note_off(screen, color, position):
    pygame.draw.circle(screen, white_off, position, 30)
    pygame.draw.circle(screen, color, position, 28)
    pygame.draw.circle(screen, black, position, 14)
    pygame.draw.circle(screen, white_off, position, 11)
    

if __name__ == '__main__':

    args = arg_parser()
    
    
    # read file
    f = open(args.chart_file, 'r')
    chart_data = f.read().replace('  ', '')
    f.close()

    search_string = '[ExpertSingle]\n{\n'
    inf = chart_data.find(search_string)
    sup = chart_data[inf:].find('}')

    sup += inf
    inf += len(search_string)

    notes_data = chart_data[inf:sup]

    notes = []

    for line in notes_data.splitlines():
        n = line.split()
        
        if (n[2] == 'N'):
            note = Note()
            note.start = int(n[0])
            note.color = int(n[3])
            note.duration = int(n[4])
            notes.append(note)
        


    pygame.init()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    running = True


    global_y_offset = 0
        
    while running:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[pygame.K_UP]:
            global_y_offset -= 1
            
        if pressed_keys[pygame.K_DOWN]:
            global_y_offset += 1
                
        screen.fill((0, 0, 0))
        
        # draw guitar neck
        pygame.draw.rect(screen, (50, 50, 50), (160, 0, 320, SCREEN_HEIGHT))
        
        # draw frets
        for i in range(5):
            y_offset = (i * 256) + global_y_offset
            pygame.draw.rect(screen, (180, 180, 180), (160, SCREEN_HEIGHT-y_offset-30-2, 320, 4))
            pygame.draw.rect(screen, (100, 100, 100), (160, SCREEN_HEIGHT-y_offset+128-30-2, 320, 4))
        
        # neck borders
        pygame.draw.rect(screen, (200, 200, 200), (140, 0, 20, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (200, 200, 200), (480, 0, 20, SCREEN_HEIGHT))
        
        # draw base notes
        for i in range(0, 5):
            draw_note_off(screen, color_off[i], (color_x_pos[i], SCREEN_HEIGHT-0-30))
        
        # draw song notes
        for note in notes:
            # TODO: change by song.resolution
            y = (256 * note.start // DEFAULT_RESOLUTION) + global_y_offset
            h = 256 * note.duration // DEFAULT_RESOLUTION
            
            pygame.draw.rect(screen, color_on[note.color], (color_x_pos[note.color]-10, SCREEN_HEIGHT-y-30-h, 20, h))
            draw_note_on(screen, color_on[note.color], (color_x_pos[note.color], SCREEN_HEIGHT-y-30))
            
        pygame.display.flip()
        
        
    pygame.quit()

