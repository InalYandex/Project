import pygame
import sys


pygame.init()

WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (34, 139, 34)

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Флэппи Берд")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLUE)

    pygame.draw.rect(screen, GREEN, (0, 400, WIDTH, HEIGHT - 400))

    pygame.display.flip()

pygame.quit()
sys.exit()