import pygame
import random

# --- Инициализация ---
pygame.init()

WIDTH, HEIGHT = 600, 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Arial", 20)

# --- Начальные параметры ---
snake = [(100, 100)]
direction = (CELL, 0)

food = None

score = 0
level = 1
speed = 10


# --- Генерация еды (НЕ на змее) ---
def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        # Проверка: еда не на змее
        if (x, y) not in snake:
            return (x, y)


food = generate_food()


# --- Основной цикл ---
running = True
while running:
    screen.fill(BLACK)

    # --- Обработка событий ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL):
                direction = (0, -CELL)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                direction = (0, CELL)
            elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                direction = (-CELL, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                direction = (CELL, 0)

    # --- Движение змеи ---
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)

    # --- Проверка столкновения со стеной ---
    if (
        head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT
    ):
        print("Game Over: Wall collision")
        running = False

    # --- Проверка столкновения с собой ---
    if head in snake[1:]:
        print("Game Over: Self collision")
        running = False

    # --- Проверка еды ---
    if head == food:
        score += 1

        # --- Повышение уровня ---
        if score % 4 == 0:   # каждые 4 еды
            level += 1
            speed += 2       # увеличение скорости

        food = generate_food()
    else:
        snake.pop()  # если не съели — хвост уменьшается

    # --- Отрисовка змеи ---
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL, CELL))

    # --- Отрисовка еды ---
    pygame.draw.rect(screen, RED, (*food, CELL, CELL))

    # --- Отображение текста ---
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 30))

    pygame.display.flip()

    # --- Скорость игры ---
    clock.tick(speed)

pygame.quit()