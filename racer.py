import pygame, random

pygame.init()  # запуск pygame

# --- размеры окна ---
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # создание окна
pygame.display.set_caption("Racer")  # название игры
clock = pygame.time.Clock()  # контроль FPS

# --- цвета ---
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# --- загрузка изображений машин ---
player_img = pygame.image.load("car.png")  # машина игрока
player_img = pygame.transform.scale(player_img, (40, 80))  # изменение размера

enemy_img = pygame.image.load("enemy.png")  # машина врага
enemy_img = pygame.transform.scale(enemy_img, (40, 80))

# --- создание прямоугольников (hitbox для collision) ---
player = player_img.get_rect(center=(200, 500))  # позиция игрока
enemy = enemy_img.get_rect(center=(random.randint(80, 320), -100))  # враг сверху

# --- скорости ---
player_speed = 5
enemy_speed = 5

# --- монеты ---
coins = []      # список монет
score = 0       # количество собранных монет
coin_timer = 0  # таймер появления монет

font = pygame.font.SysFont("Arial", 24)  # шрифт

line_y = 0  # смещение разметки (для анимации)

# --- параметры наклона машины ---
tilt_angle = 0
tilt_speed = 4
max_tilt = 12

# --- состояние игры ---
game_over = False

# --- список частиц дыма ---
smoke_particles = []


# --- функция создания монеты ---
def spawn_coin():
    return [random.randint(100, 260), -20]  # случайная позиция сверху


# --- функция создания дыма ---
def spawn_smoke(x, y):
    # создаёт несколько частиц дыма
    for _ in range(10):
        smoke_particles.append({
            "x": x,
            "y": y,
            "dx": random.randint(-2, 2),  # движение по X
            "dy": random.randint(-3, -1), # движение вверх
            "size": random.randint(5, 12),
            "life": 30  # время жизни частицы
        })


# --- функция перезапуска игры ---
def reset():
    global player, enemy, coins, score, coin_timer, enemy_speed, game_over, smoke_particles

    player.center = (200, 500)  # возвращаем игрока
    enemy.center = (random.randint(80, 320), -100)  # новый враг

    coins.clear()  # очищаем монеты
    smoke_particles.clear()  # очищаем дым

    score = 0
    coin_timer = 0
    enemy_speed = 5
    game_over = False


running = True

# --- основной игровой цикл ---
while running:
    screen.fill(WHITE)  # очистка экрана

    # --- обработка событий ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # рестарт при нажатии R
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset()

    # --- логика игры ---
    if not game_over:

        # --- управление ---
        keys = pygame.key.get_pressed()
        move = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])

        player.x += move * player_speed  # движение
        player.x = max(50, min(player.x, WIDTH - 50))  # границы

        # --- наклон машины ---
        if move != 0:
            tilt_angle -= move * tilt_speed
        else:
            # плавное возвращение в центр
            if tilt_angle > 0:
                tilt_angle -= 2
            elif tilt_angle < 0:
                tilt_angle += 2

        tilt_angle = max(-max_tilt, min(max_tilt, tilt_angle))

        # --- движение врага ---
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemy.center = (random.randint(80, 320), -100)

        # --- генерация монет ---
        coin_timer += 1
        if coin_timer >= 30:
            coins.append(spawn_coin())
            coin_timer = 0

        # --- движение монет вниз ---
        coins = [[x, y+5] for x, y in coins if y < HEIGHT]

        # --- сбор монет ---
        new_coins = []
        for x, y in coins:
            rect = pygame.Rect(x, y, 20, 20)

            if player.colliderect(rect):
                score += 1

                # каждые 5 монет увеличиваем скорость врага
                if score % 5 == 0:
                    enemy_speed += 1
            else:
                new_coins.append([x, y])

        coins = new_coins

        # --- столкновение ---
        if player.colliderect(enemy):
            game_over = True
            spawn_smoke(player.centerx, player.centery)

    # --- разметка дороги ---
    line_y += enemy_speed
    if line_y > 40:
        line_y = 0

    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 5, i + line_y, 10, 20))

    # --- отрисовка игрока с наклоном ---
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
        pygame.draw.circle(screen, (80, 80, 80),
                           (int(p["x"]), int(p["y"])), p["size"])
        p["x"] += p["dx"]
        p["y"] += p["dy"]
        p["life"] -= 1

        if p["life"] <= 0:
            smoke_particles.remove(p)

    # --- счёт ---
    screen.blit(font.render(f"Coins: {score}", True, BLACK), (WIDTH-130, 10))

    # --- экран аварии ---
    if game_over:
        screen.blit(font.render("CRASH! Press R", True, (200, 0, 0)),
                    (WIDTH//2 - 100, HEIGHT//2))

    pygame.display.flip()  # обновление экрана
    clock.tick(60)  # FPS

pygame.quit()  # завершение программы