import pygame
import random

pygame.init()

# --- настройки экрана ---
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

# --- цвета ---
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)

# --- игрок ---
player = pygame.Rect(180, 500, 40, 60)
player_speed = 5

# --- враг ---
enemy = pygame.Rect(random.randint(100, 260), -100, 40, 60)
enemy_speed = 5

# --- монеты ---
coins = []
coin_radius = 10
coin_spawn_delay = 30
coin_timer = 0

score = 0

font = pygame.font.SysFont("Arial", 24)


# --- генерация монеты ---
def spawn_coin():
    x = random.randint(100, 260)
    y = -20
    return [x, y]


# --- основной цикл ---
running = True
while running:

    screen.fill((50, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- управление игроком ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 100:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < 300:
        player.x += player_speed

    # --- движение врага ---
    enemy.y += enemy_speed
    if enemy.y > HEIGHT:
        enemy.y = -100
        enemy.x = random.randint(100, 260)

    # --- спавн монет ---
    coin_timer += 1
    if coin_timer >= coin_spawn_delay:
        coins.append(spawn_coin())
        coin_timer = 0

    # --- движение монет ---
    for coin in coins:
        coin[1] += 5

    # --- проверка сбора монет ---
    for coin in coins[:]:
        coin_rect = pygame.Rect(coin[0], coin[1], 20, 20)

        if player.colliderect(coin_rect):
            coins.remove(coin)
            score += 1

    # --- удаление монет вне экрана ---
    coins = [c for c in coins if c[1] < HEIGHT]

    # --- collision с врагом ---
    if player.colliderect(enemy):
        print("GAME OVER")
        running = False

    # --- отрисовка ---
    pygame.draw.rect(screen, (0, 0, 255), player)
    pygame.draw.rect(screen, (255, 0, 0), enemy)

    # --- рисуем монеты ---
    for coin in coins:
        pygame.draw.circle(screen, YELLOW, (coin[0], coin[1]), coin_radius)

    # --- отображение счёта ---
    score_text = font.render(f"Coins: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 120, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()