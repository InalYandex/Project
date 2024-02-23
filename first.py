import pygame
import sys
import random

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

OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = random.randint(100, 400)
OBSTACLE_X = WIDTH
OBSTACLE_Y = HEIGHT - OBSTACLE_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

background_img = pygame.image.load("prosto.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
bird_img = pygame.image.load("bыыыird.png")
bird_img = pygame.transform.scale(bird_img, (BIRD_SIZE, BIRD_SIZE))

clock = pygame.time.Clock()


def draw_obstacle(x, height):
    pygame.draw.rect(screen, GREEN, (x, 0, OBSTACLE_WIDTH, height))
    pygame.draw.rect(screen, GREEN, (x, height + 200, OBSTACLE_WIDTH, HEIGHT - height - 200))


def game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Начать заново? Нажми пробел", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 400, HEIGHT // 2 - 50))
    pygame.display.flip()
    wait_for_restart()


def wait_for_restart():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    waiting = False


def reset_game():
    global BIRD_Y, OBSTACLE_X, OBSTACLE_HEIGHT, obstacle_passed, bird_y_change

    BIRD_Y = HEIGHT // 2 - BIRD_SIZE // 2
    bird_y_change = 0
    OBSTACLE_X = WIDTH
    OBSTACLE_HEIGHT = random.randint(100, 400)
    obstacle_passed = False


bird_y_change = 0
obstacle_speed = 5
obstacle_passed = False

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

    screen.blit(background_img, (0, 0))

    draw_obstacle(OBSTACLE_X, OBSTACLE_HEIGHT)
    OBSTACLE_X -= obstacle_speed

    if OBSTACLE_X < -OBSTACLE_WIDTH:
        OBSTACLE_X = WIDTH
        OBSTACLE_HEIGHT = random.randint(100, 400)
        obstacle_passed = False

    screen.blit(bird_img, (BIRD_X, BIRD_Y))

    if BIRD_X + BIRD_SIZE > OBSTACLE_X and BIRD_X < OBSTACLE_X + OBSTACLE_WIDTH:
        if BIRD_Y < OBSTACLE_HEIGHT or BIRD_Y + BIRD_SIZE > OBSTACLE_HEIGHT + 200:
            game_over()

    pygame.display.flip()

    clock.tick(30)
