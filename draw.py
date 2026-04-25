import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    brush_size = 5
    color_map = {'r': (255, 0, 0), 'g': (0, 255, 0), 'b': (0, 0, 255)}
    tool_map = {'1': 'brush', '2': 'rect', '3': 'circle', '4': 'eraser'}

    current_color = color_map['b']
    current_tool = 'brush'

    points, start = [], None

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                key = pygame.key.name(event.key)

                if key in color_map:
                    current_color = color_map[key]
                elif key in tool_map:
                    current_tool = tool_map[key]

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                start = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                end = event.pos

                if current_tool == 'rect' and start:
                    pygame.draw.rect(screen, current_color,
                                     (*start, end[0]-start[0], end[1]-start[1]), 2)

                elif current_tool == 'circle' and start:
                    dx, dy = end[0]-start[0], end[1]-start[1]
                    pygame.draw.circle(screen, current_color,
                                       start, int((dx**2 + dy**2)**0.5), 2)

                start = None

            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                if current_tool == 'brush':
                    points.append(event.pos)
                    points = points[-256:]
                elif current_tool == 'eraser':
                    pygame.draw.circle(screen, (0, 0, 0), event.pos, brush_size*2)

        if current_tool == 'brush':
            for a, b in zip(points, points[1:]):
                draw_line(screen, a, b, brush_size, current_color)

        pygame.display.flip()
        clock.tick(60)


def draw_line(screen, start, end, size, color):
    dx, dy = start[0]-end[0], start[1]-end[1]
    steps = max(abs(dx), abs(dy))

    for i in range(steps):
        t = i/steps if steps else 0
        x = int(start[0]*(1-t) + end[0]*t)
        y = int(start[1]*(1-t) + end[1]*t)
        pygame.draw.circle(screen, color, (x, y), size)


main()