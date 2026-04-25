import pygame, random

pygame.init()

WIDTH, HEIGHT, CELL = 600, 400, 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE, GREEN, RED, BLACK = (255,255,255), (0,200,0), (200,0,0), (0,0,0)
font = pygame.font.SysFont("Arial", 20)

snake = [(100, 100)]
direction = (CELL, 0)

score, level, speed = 0, 1, 10


def generate_food():
    while True:
        pos = (random.randrange(0, WIDTH, CELL),
               random.randrange(0, HEIGHT, CELL))
        if pos not in snake:
            return pos


food = generate_food()

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            moves = {
                pygame.K_UP: (0, -CELL),
                pygame.K_DOWN: (0, CELL),
                pygame.K_LEFT: (-CELL, 0),
                pygame.K_RIGHT: (CELL, 0)
            }
            if event.key in moves:
                new_dir = moves[event.key]
                if (new_dir[0] != -direction[0] or new_dir[1] != -direction[1]):
                    direction = new_dir

    # движение
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    # collision
    if (head in snake or
        not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT)):
        print("Game Over")
        break

    snake.insert(0, head)

    # еда
    if head == food:
        score += 1
        if score % 4 == 0:
            level += 1
            speed += 2
        food = generate_food()
    else:
        snake.pop()

    # отрисовка
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (x, y, CELL, CELL))

    pygame.draw.rect(screen, RED, (*food, CELL, CELL))

    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Level: {level}", True, WHITE), (10, 30))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()