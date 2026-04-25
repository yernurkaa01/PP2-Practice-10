import pygame

def main():
    pygame.init()  # инициализация pygame

    screen = pygame.display.set_mode((640, 480))  # создание окна
    clock = pygame.time.Clock()  # контроль FPS

    brush_size = 5  # толщина кисти

    # --- словарь цветов (по клавишам) ---
    color_map = {
        'r': (255, 0, 0),   # красный
        'g': (0, 255, 0),   # зелёный
        'b': (0, 0, 255)    # синий
    }

    # --- словарь инструментов ---
    tool_map = {
        '1': 'brush',   # кисть
        '2': 'rect',    # прямоугольник
        '3': 'circle',  # круг
        '4': 'eraser'   # ластик
    }

    current_color = color_map['b']  # текущий цвет (по умолчанию синий)
    current_tool = 'brush'  # текущий инструмент

    points = []  # список точек для рисования линии
    start = None  # начальная точка фигуры

    while True:
        for event in pygame.event.get():

            # --- выход из программы ---
            if event.type == pygame.QUIT:
                return

            # --- обработка клавиатуры ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                key = pygame.key.name(event.key)  # получаем нажатую клавишу

                # смена цвета
                if key in color_map:
                    current_color = color_map[key]

                # смена инструмента
                elif key in tool_map:
                    current_tool = tool_map[key]

            # --- нажатие мыши ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                start = event.pos  # запоминаем начальную точку

            # --- отпускание мыши ---
            if event.type == pygame.MOUSEBUTTONUP:
                end = event.pos  # конечная точка

                # --- рисование прямоугольника ---
                if current_tool == 'rect' and start:
                    pygame.draw.rect(
                        screen,
                        current_color,
                        (*start, end[0] - start[0], end[1] - start[1]),
                        2  # толщина линии
                    )

                # --- рисование круга ---
                elif current_tool == 'circle' and start:
                    dx, dy = end[0] - start[0], end[1] - start[1]
                    radius = int((dx**2 + dy**2) ** 0.5)

                    pygame.draw.circle(
                        screen,
                        current_color,
                        start,
                        radius,
                        2
                    )

                start = None  # сбрасываем начальную точку

            # --- движение мыши ---
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:

                # кисть (рисуем линию)
                if current_tool == 'brush':
                    points.append(event.pos)
                    points = points[-256:]  # ограничиваем длину списка

                # ластик (рисуем чёрным цветом)
                elif current_tool == 'eraser':
                    pygame.draw.circle(screen, (0, 0, 0),
                                       event.pos, brush_size * 2)

        # --- отрисовка линий кистью ---
        if current_tool == 'brush':
            for a, b in zip(points, points[1:]):
                draw_line(screen, a, b, brush_size, current_color)

        pygame.display.flip()  # обновление экрана
        clock.tick(60)  # FPS


# --- функция рисования линии между двумя точками ---
def draw_line(screen, start, end, size, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]

    steps = max(abs(dx), abs(dy))  # количество шагов

    for i in range(steps):
        t = i / steps if steps else 0  # прогресс от 0 до 1

        # линейная интерполяция координат
        x = int(start[0] * (1 - t) + end[0] * t)
        y = int(start[1] * (1 - t) + end[1] * t)

        pygame.draw.circle(screen, color, (x, y), size)


main()