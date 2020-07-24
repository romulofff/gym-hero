import pygame

black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((400, 400))

img = pygame.image.load('../chart.png')
img_rect = img.get_rect().size
# img.convert()

clock = pygame.time.Clock()

x = y = 0
while True:
    # screen.fill(black)
    if y == 400-img_rect[1]:
        pygame.quit()
        break
    y -= 1
    screen.blit(img, (x,y))
    pygame.display.flip()

    clock.tick(144)
