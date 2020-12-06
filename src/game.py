import pygame
from pygame import mixer
import math
import random
from os import path


def EuclidianDistance(x1,y1, x2,y2):
    return math.sqrt((math.pow(x1-x2,2)) + (math.pow(y1 - y2,2)))

def Collision(BlockX, BlockY, ButtonX, ButtonY):
    distance = EuclidianDistance(BlockX, BlockY, ButtonX, ButtonY)
    if distance < 72:
        return True
    else:
        return False

class Note(pygame.sprite.Sprite):
    def __init__(self, img, imgX, imgY):
        super().__init__()

        self.img = img
        pygame.transform.scale(self.img, (60, 60))
        self.rect = self.img.get_rect()
        print(self.rect)
    
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))

# RED bites
redImg = pygame.image.load(
    path.join('..', 'assets', 'redbutton.png')).convert()
redX = 274
# redY = random.randint(-1472, -128)  # randomizes intial y-position
redY = 100  # randomizes intial y-position
redChange = random.uniform(2, 3)  # randomizes intial speed
red_block = Note(redImg, redX, redY)

block_list = pygame.sprite.Group()
