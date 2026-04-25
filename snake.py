import pygame, random

pygame.init()  # инициализация pygame

# --- размеры окна и клетки ---
WIDTH, HEIGHT, CELL = 600, 400, 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # создание окна
pygame.display.set_caption("Snake")  # название окна

clock = pygame.time.Clock()  # контроль FPS
font = pygame.font.SysFont("Arial", 24)  # шрифт для текста

# --- цвета ---
WHITE = (255,255,255)
GREEN = (0,200,0)
RED = (200,0,0)
BLACK = (0,0,0)
GRAY = (40,40,40)

# --- начальное состояние змейки ---
snake = [(100, 100)]  # список координат сегментов (голова = первый элемент)
direction = (CELL, 0)  # начальное направление движения

# --- игровые параметры ---
score, level, speed = 0, 1, 10


# --- функция генерации еды ---
def spawn_food():
    while True:
        # случайная позиция по сетке
        pos = (random.randrange(0, WIDTH, CELL),
               random.randrange(0, HEIGHT, CELL))
        
        # проверка: еда не должна появляться на змее
        if pos not in snake:
            return pos


food = spawn_food()  # первая еда


# --- функция отрисовки сетки ---
def draw_grid():
    # вертикальные линии
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    
    # горизонтальные линии
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


running = True
game_over = False  # флаг окончания игры


# --- основной игровой цикл ---
while running:
    screen.fill(BLACK)  # очистка экрана

    # --- обработка событий ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- управление клавиатурой ---
        if event.type == pygame.KEYDOWN:
            
            # возможные направления
            moves = {
                pygame.K_UP: (0, -CELL),
                pygame.K_DOWN: (0, CELL),
                pygame.K_LEFT: (-CELL, 0),
                pygame.K_RIGHT: (CELL, 0)
            }

            # если нажата стрелка
            if event.key in moves:
                new_dir = moves[event.key]
                
                # запрет движения назад (в себя)
                if (new_dir[0] != -direction[0] or new_dir[1] != -direction[1]):
                    direction = new_dir

            # --- рестарт игры ---
            if game_over and event.key == pygame.K_r:
                snake = [(100, 100)]
                direction = (CELL, 0)
                score, level, speed = 0, 1, 10
                food = spawn_food()
                game_over = False

    # --- логика игры ---
    if not game_over:
        # вычисляем новую позицию головы
        head = (snake[0][0] + direction[0],
                snake[0][1] + direction[1])

        # --- проверка столкновений ---
        if (head in snake or  # врезались в себя
            not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT)):  # вышли за границы
            game_over = True

        snake.insert(0, head)  # добавляем новую голову

        # --- проверка еды ---
        if head == food:
            score += 1  # увеличиваем счёт
            
            # каждые 4 очка повышаем уровень
            if score % 4 == 0:
                level += 1
                speed += 2  # ускорение игры
            
            food = spawn_food()  # новая еда
        else:
            snake.pop()  # удаляем хвост (если не съели)

    # --- отрисовка ---
    
    draw_grid()  # сетка

    # --- змейка ---
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (x, y, CELL, CELL), border_radius=5)

    # --- еда ---
    pygame.draw.rect(screen, RED, (*food, CELL, CELL), border_radius=5)

    # --- интерфейс ---
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Level: {level}", True, WHITE), (10, 40))

    # --- экран Game Over ---
    if game_over:
        text = font.render("GAME OVER - Press R", True, RED)
        screen.blit(text, (WIDTH//2 - 120, HEIGHT//2))

    pygame.display.flip()  # обновление экрана
    clock.tick(speed)  # управление скоростью игры

pygame.quit()  # корректное завершение pygame