import pygame, random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)

player = pygame.Rect(180, 500, 40, 60)
enemy = pygame.Rect(random.randint(100, 260), -100, 40, 60)

player_speed = 5
enemy_speed = 5

coins = []
score = 0
coin_timer = 0

font = pygame.font.SysFont("Arial", 24)


def spawn_coin():
    return [random.randint(100, 260), -20]


running = True
while running:
    screen.fill((50, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- управление ---
    keys = pygame.key.get_pressed()
    player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed
    player.x = max(100, min(player.x, 260))

    # --- враг ---
    enemy.y += enemy_speed
    if enemy.y > HEIGHT:
        enemy = pygame.Rect(random.randint(100, 260), -100, 40, 60)

    # --- монеты ---
    coin_timer += 1
    if coin_timer >= 30:
        coins.append(spawn_coin())
        coin_timer = 0

    coins = [[x, y+5] for x, y in coins if y < HEIGHT]

    # --- сбор монет ---
    new_coins = []
    for x, y in coins:
        coin_rect = pygame.Rect(x, y, 20, 20)
        if player.colliderect(coin_rect):
            score += 1
        else:
            new_coins.append([x, y])
    coins = new_coins

    # --- collision ---
    if player.colliderect(enemy):
        print("GAME OVER")
        running = False

    # --- отрисовка ---
    pygame.draw.rect(screen, (0, 0, 255), player)
    pygame.draw.rect(screen, (255, 0, 0), enemy)

    for x, y in coins:
        pygame.draw.circle(screen, YELLOW, (x, y), 10)

    screen.blit(font.render(f"Coins: {score}", True, WHITE), (WIDTH-130, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()