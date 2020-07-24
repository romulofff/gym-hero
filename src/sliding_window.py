import pygame

black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((400, 400))

img = pygame.image.load('../chart4.png')
img_rect = img.get_rect().size

clock = pygame.time.Clock()

x = 0
y = -img_rect[1]
print(x,y)
while True:
    screen.fill(black)
    if y == 400:
        pygame.quit()
        break
    y += 1
    screen.blit(img, (x,y))
    pygame.display.flip()

    clock.tick(144)
