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
GRAVITY = 1.5

OBSTACLE_WIDTH = 50
GAP = 200
OBSTACLE_GAP = 300
OBSTACLE_X = WIDTH
OBSTACLE_HEIGHT1 = random.randint(100, HEIGHT - GAP - 100)
OBSTACLE_Y1 = HEIGHT - OBSTACLE_HEIGHT1
OBSTACLE_HEIGHT2 = HEIGHT - OBSTACLE_HEIGHT1 - GAP
OBSTACLE_Y2 = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

background_img = pygame.image.load("prosto.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (BIRD_SIZE, BIRD_SIZE))

clock = pygame.time.Clock()

score = 0
font = pygame.font.Font(None, 36)


def draw_score(score):
    score_text = font.render("Счёт: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))


def draw_obstacle(x, height1, height2):
    pygame.draw.rect(screen, '#9ACD32', (x, 0, OBSTACLE_WIDTH, height1))
    pygame.draw.rect(screen, '#9ACD32', (x, height1 + GAP, OBSTACLE_WIDTH, height2))


def game_over():
    font = pygame.font.Font(None, 74)
    text = font.render(f"Вы проиграли, Счет: {score}", True, '#FFFF00')
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
    global BIRD_Y, OBSTACLE_X, OBSTACLE_HEIGHT1, OBSTACLE_HEIGHT2, obstacle_passed, bird_y_change, score

    BIRD_Y = HEIGHT // 2 - BIRD_SIZE // 2
    bird_y_change = 0
    OBSTACLE_X = WIDTH
    OBSTACLE_HEIGHT1 = random.randint(100, HEIGHT - GAP - 100)
    OBSTACLE_HEIGHT2 = HEIGHT - OBSTACLE_HEIGHT1 - GAP
    obstacle_passed = False
    score = 0


bird_y_change = 0
obstacle_speed = 30
obstacle_passed = False
time_elapsed = 0
speed_increase = 1
score_timer = 0
SCORE_UPDATE_INTERVAL = 29

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

    draw_obstacle(OBSTACLE_X, OBSTACLE_HEIGHT1, OBSTACLE_HEIGHT2)
    OBSTACLE_X -= obstacle_speed

    if OBSTACLE_X < -OBSTACLE_WIDTH:
        OBSTACLE_X = WIDTH
        OBSTACLE_HEIGHT1 = random.randint(100, HEIGHT - GAP - 100)
        OBSTACLE_HEIGHT2 = HEIGHT - OBSTACLE_HEIGHT1 - GAP
        obstacle_passed = False

    screen.blit(bird_img, (BIRD_X, BIRD_Y))

    if BIRD_X + BIRD_SIZE > OBSTACLE_X and BIRD_X < OBSTACLE_X + OBSTACLE_WIDTH:
        if BIRD_Y < OBSTACLE_HEIGHT1 or BIRD_Y + BIRD_SIZE > OBSTACLE_HEIGHT1 + GAP:
            game_over()

    time_elapsed += 1
    if time_elapsed % (30 * 30) == 0:
        obstacle_speed += speed_increase

    score_timer += 1
    if score_timer >= SCORE_UPDATE_INTERVAL:
        score += 1
        score_timer = 0

    draw_score(score)

    pygame.display.flip()

    clock.tick(30)