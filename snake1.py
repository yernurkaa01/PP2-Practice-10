import pygame, random

pygame.init()

# --- window settings ---
WIDTH, HEIGHT, CELL = 600, 400, 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# --- colors ---
WHITE = (255,255,255)
GREEN = (0,200,0)
RED = (200,0,0)
BLACK = (0,0,0)
GRAY = (40,40,40)

# --- snake ---
snake = [(100, 100)]
direction = (CELL, 0)

# --- game stats ---
score, level, speed = 0, 1, 10


# --- generate food with weight and timer ---
def spawn_food():
    while True:
        pos = (random.randrange(0, WIDTH, CELL),
               random.randrange(0, HEIGHT, CELL))
        
        if pos not in snake:
            # food weight (value)
            value = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
            
            # lifetime of food
            timer = 100
            
            return {
                "pos": pos,
                "value": value,
                "timer": timer
            }


food = spawn_food()


# --- draw grid ---
def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


running = True
game_over = False


while running:
    screen.fill(BLACK)

    # --- events ---
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

                # prevent moving backward
                if (new_dir[0] != -direction[0] or new_dir[1] != -direction[1]):
                    direction = new_dir

            # restart
            if game_over and event.key == pygame.K_r:
                snake = [(100, 100)]
                direction = (CELL, 0)
                score, level, speed = 0, 1, 10
                food = spawn_food()
                game_over = False

    # --- game logic ---
    if not game_over:
        head = (snake[0][0] + direction[0],
                snake[0][1] + direction[1])

        # collision
        if (head in snake or
            not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT)):
            game_over = True

        snake.insert(0, head)

        # --- food timer ---
        food["timer"] -= 1

        # if food expired → respawn
        if food["timer"] <= 0:
            food = spawn_food()

        # --- eating food ---
        if head == food["pos"]:
            score += food["value"]  # different weights

            if score % 4 == 0:
                level += 1
                speed += 2

            food = spawn_food()
        else:
            snake.pop()

    # --- drawing ---
    draw_grid()

    # snake
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (x, y, CELL, CELL), border_radius=5)

    # --- food drawing (size depends on weight) ---
    size = CELL - (3 - food["value"]) * 6

    pygame.draw.rect(
        screen,
        RED,
        (food["pos"][0], food["pos"][1], size, size),
        border_radius=5
    )

    # UI
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Level: {level}", True, WHITE), (10, 40))

    # game over screen
    if game_over:
        text = font.render("GAME OVER - Press R", True, RED)
        screen.blit(text, (WIDTH//2 - 120, HEIGHT//2))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()