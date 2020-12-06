import random
from os import path
import math 

import pygame
from pygame import mixer

# from mido import MidiFile


# pygame.mixer.pre_init(frequency=44100)
# pygame.init()
# sna = path.join('..', 'The White Stripes - Seven Nation Army', 'notes.mid')
sna = path.join('..', 'The White Stripes - Seven Nation Army', 'song.ogg')
# print(sna)
# mid = MidiFile(sna, clip=True)
# print(mid)

# for track in mid.tracks:
#     print(track)
# for msg in mid.tracks[3]:
#     print(msg)


pygame.init()
screen = pygame.display.set_mode((800, 600))  # creates window screen
pygame.display.set_caption("GH-PyGame") #icon and title
mixer.music.load(sna)
mixer.music.play()
mixer.music.set_volume(1)

class Note(pygame.sprite.Sprite): #note class
    def __init__(self, Img, ImgX, ImgY):
        self.Img = Img
        self.ImgX = ImgX
        self.ImgY = ImgY

    def spawn(self, Img, ImgX, ImgY):
        screen.blit(Img, (ImgX, ImgY))

# RED BLOCKS
redImg = pygame.image.load(
    path.join('..', 'assets', 'redbutton.png')).convert()
redX = 274
# redY = random.randint(-1472, -128)  # randomizes intial y-position
redY = 100  # randomizes intial y-position
redChange = random.uniform(2, 3)  # randomizes intial speed
red_block = Block(redImg, redX, redY)

def EuclidianDistance(x1,y1, x2,y2):
    return math.sqrt((math.pow(x1-x2,2)) + (math.pow(y1 - y2,2)))

def Collision(BlockX, BlockY, ButtonX, ButtonY):
    distance = EuclidianDistance(BlockX, BlockY, ButtonX, ButtonY)
    if distance < 72:
        return True
    else:
        return False

while True:
    # screen.fill((0,0,0))
    red_block.spawn(redImg, redX, redY)
    pygame.display.flip()
    