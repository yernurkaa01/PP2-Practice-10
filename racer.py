import pygame, random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# --- загрузка машин ---
player_img = pygame.image.load("car.png")
player_img = pygame.transform.scale(player_img, (40, 80))

enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (40, 80))

player = player_img.get_rect(center=(200, 500))
enemy = enemy_img.get_rect(center=(random.randint(80, 320), -100))

player_speed = 5
enemy_speed = 5

coins = []
score = 0
coin_timer = 0

font = pygame.font.SysFont("Arial", 24)

line_y = 0

# --- наклон ---
tilt_angle = 0
tilt_speed = 4
max_tilt = 12

# --- состояние игры ---
game_over = False

# --- частицы дыма ---
smoke_particles = []


def spawn_coin():
    return [random.randint(100, 260), -20]


def spawn_smoke(x, y):
    # создаёт несколько "облаков дыма"
    for _ in range(10):
        smoke_particles.append({
            "x": x,
            "y": y,
            "dx": random.randint(-2, 2),
            "dy": random.randint(-3, -1),
            "size": random.randint(5, 12),
            "life": 30
        })


def reset():
    global player, enemy, coins, score, coin_timer, enemy_speed, game_over, smoke_particles

    player.center = (200, 500)
    enemy.center = (random.randint(80, 320), -100)

    coins.clear()
    smoke_particles.clear()

    score = 0
    coin_timer = 0
    enemy_speed = 5
    game_over = False


running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset()

    if not game_over:
        # --- управление ---
        keys = pygame.key.get_pressed()
        move = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])

        player.x += move * player_speed
        player.x = max(50, min(player.x, WIDTH - 50))

        # --- наклон ---
        if move != 0:
            tilt_angle -= move * tilt_speed
        else:
            if tilt_angle > 0:
                tilt_angle -= 2
            elif tilt_angle < 0:
                tilt_angle += 2

        tilt_angle = max(-max_tilt, min(max_tilt, tilt_angle))

        # --- враг ---
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemy.center = (random.randint(80, 320), -100)

        # --- монеты ---
        coin_timer += 1
        if coin_timer >= 30:
            coins.append(spawn_coin())
            coin_timer = 0

        coins = [[x, y+5] for x, y in coins if y < HEIGHT]

        # --- сбор ---
        new_coins = []
        for x, y in coins:
            rect = pygame.Rect(x, y, 20, 20)
            if player.colliderect(rect):
                score += 1
                if score % 5 == 0:
                    enemy_speed += 1
            else:
                new_coins.append([x, y])
        coins = new_coins

        # --- столкновение ---
        if player.colliderect(enemy):
            game_over = True
            spawn_smoke(player.centerx, player.centery)

    # --- разметка ---
    line_y += enemy_speed
    if line_y > 40:
        line_y = 0

    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 5, i + line_y, 10, 20))

    # --- отрисовка игрока ---
    rotated = pygame.transform.rotate(player_img, tilt_angle)
    rect = rotated.get_rect(center=player.center)
    screen.blit(rotated, rect)

    # --- враг ---
    screen.blit(enemy_img, enemy)

    # --- монеты ---
    for x, y in coins:
        pygame.draw.circle(screen, YELLOW, (x, y), 10)

    # --- дым ---
    for p in smoke_particles[:]:
        pygame.draw.circle(screen, (80, 80, 80), (int(p["x"]), int(p["y"])), p["size"])
        p["x"] += p["dx"]
        p["y"] += p["dy"]
        p["life"] -= 1
        if p["life"] <= 0:
            smoke_particles.remove(p)

    # --- текст ---
    screen.blit(font.render(f"Coins: {score}", True, BLACK), (WIDTH-130, 10))

    if game_over:
        screen.blit(font.render("CRASH! Press R", True, (200, 0, 0)),
                    (WIDTH//2 - 100, HEIGHT//2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()