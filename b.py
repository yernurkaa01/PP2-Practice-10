import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 5
    mode = 'blue'
    tool = 'brush'  # brush, rect, circle, eraser

    points = []
    start_pos = None

    while True:
        pressed = pygame.key.get_pressed()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                # --- выбор цвета ---
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'

                # --- выбор инструмента ---
                elif event.key == pygame.K_1:
                    tool = 'brush'
                elif event.key == pygame.K_2:
                    tool = 'rect'
                elif event.key == pygame.K_3:
                    tool = 'circle'
                elif event.key == pygame.K_4:
                    tool = 'eraser'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                end_pos = event.pos

                # --- Рисование фигур ---
                if tool == 'rect' and start_pos:
                    pygame.draw.rect(screen, get_color(mode),
                                     (*start_pos,
                                      end_pos[0] - start_pos[0],
                                      end_pos[1] - start_pos[1]), 2)

                elif tool == 'circle' and start_pos:
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    radius_circle = int((dx**2 + dy**2) ** 0.5)
                    pygame.draw.circle(screen, get_color(mode),
                                       start_pos, radius_circle, 2)

                start_pos = None

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:

                    if tool == 'brush':
                        points.append(event.pos)
                        points = points[-256:]

                    elif tool == 'eraser':
                        pygame.draw.circle(screen, (0, 0, 0),
                                           event.pos, radius * 2)

        # --- рисование линий ---
        if tool == 'brush':
            i = 0
            while i < len(points) - 1:
                drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
                i += 1

        pygame.display.flip()
        clock.tick(60)


def get_color(mode):
    if mode == 'blue':
        return (0, 0, 255)
    elif mode == 'red':
        return (255, 0, 0)
    elif mode == 'green':
        return (0, 255, 0)


def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = i / iterations if iterations != 0 else 0
        x = int(start[0] * (1 - progress) + end[0] * progress)
        y = int(start[1] * (1 - progress) + end[1] * progress)
        pygame.draw.circle(screen, color, (x, y), width)


main()