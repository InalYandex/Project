import pygame
import sys

pygame.init()

WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (34, 139, 34)

WIDTH, HEIGHT = 800, 600
BIRD_SIZE = 50
BIRD_X = 100
BIRD_Y = HEIGHT // 2 - BIRD_SIZE // 2
BIRD_JUMP = 10
GRAVITY = 1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

def draw_bird(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, BIRD_SIZE, BIRD_SIZE))

def game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

bird_y_change = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_y_change = -BIRD_JUMP

    bird_y_change += GRAVITY
    BIRD_Y += bird_y_change

    if BIRD_Y < 0:
        BIRD_Y = 0
    elif BIRD_Y > HEIGHT - BIRD_SIZE:
        game_over()

    screen.fill(BLUE)

    draw_bird(BIRD_X, BIRD_Y)

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
sys.exit()
