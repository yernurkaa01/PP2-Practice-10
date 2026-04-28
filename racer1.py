import pygame, random

pygame.init()

# --- window ---
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

# --- colors ---
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# --- images ---
player_img = pygame.image.load("car.png")
player_img = pygame.transform.scale(player_img, (40, 80))

enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (40, 80))

# --- rects ---
player = player_img.get_rect(center=(200, 500))
enemy = enemy_img.get_rect(center=(random.randint(80, 320), -100))

# --- speeds ---
player_speed = 5
enemy_speed = 5

# --- coins ---
coins = []
score = 0
coin_timer = 0

font = pygame.font.SysFont("Arial", 24)

line_y = 0

tilt_angle = 0
tilt_speed = 4
max_tilt = 12

game_over = False


# --- spawn coin with different weights ---
def spawn_coin():
    # value of coin (weight)
    value = random.choices([1, 2, 3], weights=[60, 30, 10])[0]

    x = random.randint(100, 260)
    y = -20

    return [x, y, value]


# --- reset game ---
def reset():
    global player, enemy, coins, score, coin_timer, enemy_speed, game_over

    player.center = (200, 500)
    enemy.center = (random.randint(80, 320), -100)

    coins.clear()
    score = 0
    coin_timer = 0
    enemy_speed = 5
    game_over = False


running = True

while running:
    screen.fill(WHITE)

    # --- events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset()

    if not game_over:

        # --- movement ---
        keys = pygame.key.get_pressed()
        move = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])

        player.x += move * player_speed
        player.x = max(50, min(player.x, WIDTH - 50))

        # --- enemy ---
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemy.center = (random.randint(80, 320), -100)

        # --- spawn coins ---
        coin_timer += 1
        if coin_timer >= 30:
            coins.append(spawn_coin())
            coin_timer = 0

        # --- move coins ---
        coins = [[x, y+5, value] for x, y, value in coins if y < HEIGHT]

        # --- collect coins ---
        new_coins = []
        for x, y, value in coins:
            rect = pygame.Rect(x, y, 20, 20)

            if player.colliderect(rect):
                score += value  # different weights

                # increase enemy speed every N coins
                if score % 5 == 0:
                    enemy_speed += 1
            else:
                new_coins.append([x, y, value])

        coins = new_coins

        # --- collision ---
        if player.colliderect(enemy):
            game_over = True

    # --- road ---
    line_y += enemy_speed
    if line_y > 40:
        line_y = 0

    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 5, i + line_y, 10, 20))

    # --- player ---
    rotated = pygame.transform.rotate(player_img, tilt_angle)
    rect = rotated.get_rect(center=player.center)
    screen.blit(rotated, rect)

    # --- enemy ---
    screen.blit(enemy_img, enemy)

    # --- draw coins ---
    for x, y, value in coins:
        radius = 6 + value * 4  # different size for weight
        pygame.draw.circle(screen, YELLOW, (x, y), radius)

    # --- score ---
    screen.blit(font.render(f"Coins: {score}", True, BLACK), (WIDTH-130, 10))

    # --- crash ---
    if game_over:
        screen.blit(font.render("CRASH! Press R", True, (200, 0, 0)),
                    (WIDTH//2 - 100, HEIGHT//2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()