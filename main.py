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
BIRD_JUMP = 9
GRAVITY = 1.5

OBSTACLE_WIDTH = 50
GAP = 200
OBSTACLE_GAP = 300
OBSTACLE_X = WIDTH
OBSTACLE_HEIGHT1 = random.randint(100, HEIGHT - GAP - 100)
OBSTACLE_Y1 = HEIGHT - OBSTACLE_HEIGHT1
OBSTACLE_HEIGHT2 = HEIGHT - OBSTACLE_HEIGHT1 - GAP
OBSTACLE_Y2 = 0

HORIZONTAL_OBSTACLE_WIDTH = 200
HORIZONTAL_OBSTACLE_HEIGHT = 20
HORIZONTAL_OBSTACLE_Y = 150
HORIZONTAL_OBSTACLE_X = WIDTH
HORIZONTAL_OBSTACLE_SPEED = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

background_img = pygame.image.load("prosto.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (BIRD_SIZE, BIRD_SIZE))

clock = pygame.time.Clock()


class Obstacle:
    def __init__(self, x, height1, height2):
        self.x = x
        self.height1 = height1
        self.height2 = height2

    def update_position(self):
        self.x -= HORIZONTAL_OBSTACLE_SPEED
        if self.x < -OBSTACLE_WIDTH:
            self.x = WIDTH
            self.height1 = random.randint(100, HEIGHT - GAP - 100)
            self.height2 = HEIGHT - self.height1 - GAP


def draw_obstacle(x, height1, height2):
    pygame.draw.rect(screen, GREEN, (x, 0, OBSTACLE_WIDTH, height1))
    pygame.draw.rect(screen, GREEN, (x, height1 + GAP, OBSTACLE_WIDTH, height2))


def game_over():
    global counter
    counter = 0
    reset_game()
    BIRD_Y = HEIGHT // 2 - BIRD_SIZE // 2
    BIRD_X = WIDTH - BIRD_SIZE
    font = pygame.font.Font(None, 74)
    text = font.render("Вы проиграли. Нажмите пробел", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 400, HEIGHT // 2 - 50))

    draw_obstacle(obstacle1.x, obstacle1.height1, obstacle1.height2)

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
    global BIRD_Y, OBSTACLE_X, OBSTACLE_HEIGHT1, OBSTACLE_HEIGHT2, obstacle_passed, bird_y_change

    BIRD_Y = HEIGHT // 2 - BIRD_SIZE // 2
    bird_y_change = 0
    OBSTACLE_X = WIDTH
    OBSTACLE_HEIGHT1 = random.randint(100, HEIGHT - GAP - 100)
    OBSTACLE_HEIGHT2 = HEIGHT - OBSTACLE_HEIGHT1 - GAP
    obstacle_passed = False


bird_y_change = 0
obstacle_speed = 5
obstacle_passed = False
time_elapsed = 0
speed_increase = 1
counter = 0

obstacle1 = Obstacle(OBSTACLE_X, OBSTACLE_HEIGHT1, OBSTACLE_HEIGHT2)
horizontal_obstacle = Obstacle(HORIZONTAL_OBSTACLE_X, HORIZONTAL_OBSTACLE_Y, HORIZONTAL_OBSTACLE_HEIGHT)

font = pygame.font.Font(None, 36)

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

    draw_obstacle(obstacle1.x, obstacle1.height1, obstacle1.height2)
    obstacle1.update_position()

    horizontal_obstacle.update_position()

    if obstacle1.x < -OBSTACLE_WIDTH:
        obstacle1.x = WIDTH
        obstacle1.height1 = random.randint(100, HEIGHT - GAP - 100)
        obstacle1.height2 = HEIGHT - obstacle1.height1 - GAP
        obstacle_passed = False

    screen.blit(bird_img, (BIRD_X, BIRD_Y))

    if (BIRD_X + BIRD_SIZE > obstacle1.x and BIRD_X < obstacle1.x + OBSTACLE_WIDTH) \
            and (BIRD_Y < obstacle1.height1 or BIRD_Y + BIRD_SIZE > obstacle1.height1 + GAP):
        game_over()

    if (BIRD_Y < horizontal_obstacle.height1 + HORIZONTAL_OBSTACLE_HEIGHT and
            BIRD_Y + BIRD_SIZE > horizontal_obstacle.height1 and
            BIRD_X + BIRD_SIZE > horizontal_obstacle.x and
            BIRD_X < horizontal_obstacle.x + HORIZONTAL_OBSTACLE_WIDTH):
        game_over()

    time_elapsed += 1
    if time_elapsed == 210:
        counter += 1
        time_elapsed = 0

    counter_text = font.render(f"Счет: {counter}", True, WHITE)
    screen.blit(counter_text, (10, 10))
    pygame.display.flip()

    clock.tick(30)
