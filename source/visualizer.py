import os
import cv2
import pygame

# GAME SETUP
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.HIDDEN)
FPS = 60
DELAY = 10
LONGDELAY = 1000

# DEFINE COLOR
WHITE = (255, 255, 255)

# CONSTANTS
CELL_WIDTH, CELL_HEIGHT = 50, 50
dx = [1, -1, 0, 0] # direction x
dy = [0, 0, 1, -1] # direction y
ROW, COL = 0, 0
X_OFFSET, Y_OFFSET = 0, 0

# INCLUDE IMAGE
START_IMG = pygame.image.load(os.path.join('..', 'Assets', 'start.jpg'))
END_IMG = pygame.image.load(os.path.join('..', 'Assets', 'door.jpg'))
WALL_IMG = pygame.image.load(os.path.join('..', 'Assets', 'wall.jpg'))
VISITED_IMG = pygame.image.load(os.path.join('..', 'Assets', 'visited.jpg'))
PATH_IMG = pygame.image.load(os.path.join('..', 'Assets', 'path.jpg'))
START_CHECK_IMG = pygame.image.load(os.path.join('..', 'Assets', 'start_checked.png'))
DOOR_OPEN = pygame.image.load(os.path.join('..', 'Assets', 'door_checked.png'))
TELEPORT_IN_IMG = pygame.image.load(os.path.join('..', 'Assets', 'teleport_in.png'))
TELEPORT_OUT_IMG = pygame.image.load(os.path.join('..', 'Assets', 'teleport_out.png'))
TELEPORT_IN_VISITED_IMG = pygame.image.load(os.path.join('..', 'Assets', 'teleport_in_visited.png'))
TELEPORT_OUT_VISITED_IMG = pygame.image.load(os.path.join('..', 'Assets', 'teleport_out_visited.png'))
STATION_CHECK_IMG = pygame.image.load(os.path.join('..', 'Assets', 'bus_stop_checked.png'))
GIFT_IMG = pygame.image.load(os.path.join('..', 'Assets', 'gift.jpg'))
GIFT_CHECKED_IMG = pygame.image.load(os.path.join('..', 'Assets', 'gift_checked.png'))
NUMBER0_IMG = pygame.image.load(os.path.join('..', 'Assets', 'number0.jpg'))
NUMBER1_IMG = pygame.image.load(os.path.join('..', 'Assets', 'number1.jpg'))
NUMBER2_IMG = pygame.image.load(os.path.join('..', 'Assets', 'number2.jpg'))
NUMBER3_IMG = pygame.image.load(os.path.join('..', 'Assets', 'number3.jpg'))
NUMBER4_IMG = pygame.image.load(os.path.join('..', 'Assets', 'number4.jpg'))
NUMBER5_IMG = pygame.image.load(os.path.join('..', 'Assets', 'number5.jpg'))
NUMBER6_IMG = pygame.image.load(os.path.join('..', 'Assets', 'number6.jpg'))
NUMBER7_IMG = pygame.image.load(os.path.join('..', 'Assets', 'number7.jpg'))
NUMBER8_IMG = pygame.image.load(os.path.join('..', 'Assets', 'number8.jpg'))
NUMBER9_IMG = pygame.image.load(os.path.join('..', 'Assets', 'number9.jpg'))

def scale_img(CELL_WIDTH, CELL_HEIGHT):
    # Scale all icons to fit with the pygame's map

    global START_IMG, END_IMG, GIFT_IMG, GIFT_CHECKED_IMG, WALL_IMG, VISITED_IMG, PATH_IMG, START_CHECK_IMG, DOOR_OPEN
    global TELEPORT_IN_IMG, TELEPORT_IN_VISITED_IMG, TELEPORT_OUT_IMG, TELEPORT_OUT_VISITED_IMG, STATION_CHECK_IMG
    global NUMBER0_IMG, NUMBER1_IMG, NUMBER2_IMG, NUMBER3_IMG, NUMBER4_IMG, NUMBER5_IMG, NUMBER6_IMG, NUMBER7_IMG, NUMBER8_IMG, NUMBER9_IMG 
    START_IMG = pygame.transform.scale(START_IMG, (CELL_WIDTH, CELL_HEIGHT))
    END_IMG = pygame.transform.scale(END_IMG, (CELL_WIDTH, CELL_HEIGHT))
    GIFT_IMG = pygame.transform.scale(GIFT_IMG, (CELL_WIDTH, CELL_HEIGHT))
    WALL_IMG = pygame.transform.scale(WALL_IMG, (CELL_WIDTH, CELL_HEIGHT))
    VISITED_IMG = pygame.transform.scale(VISITED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    PATH_IMG = pygame.transform.scale(PATH_IMG, (CELL_WIDTH, CELL_HEIGHT))
    START_CHECK_IMG = pygame.transform.scale(START_CHECK_IMG, (CELL_WIDTH, CELL_HEIGHT))
    DOOR_OPEN = pygame.transform.scale(DOOR_OPEN, (CELL_WIDTH, CELL_HEIGHT))
    TELEPORT_IN_IMG = pygame.transform.scale(TELEPORT_IN_IMG, (CELL_WIDTH, CELL_HEIGHT))
    TELEPORT_IN_VISITED_IMG = pygame.transform.scale(TELEPORT_IN_VISITED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    TELEPORT_OUT_IMG = pygame.transform.scale(TELEPORT_OUT_IMG, (CELL_WIDTH, CELL_HEIGHT))
    TELEPORT_OUT_VISITED_IMG = pygame.transform.scale(TELEPORT_OUT_VISITED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    STATION_CHECK_IMG = pygame.transform.scale(STATION_CHECK_IMG, (CELL_WIDTH, CELL_HEIGHT))
    GIFT_IMG = pygame.transform.scale(GIFT_IMG, (CELL_WIDTH, CELL_HEIGHT))
    GIFT_CHECKED_IMG = pygame.transform.scale(GIFT_CHECKED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    NUMBER0_IMG = pygame.transform.scale(NUMBER0_IMG, (CELL_WIDTH, CELL_HEIGHT))
    NUMBER1_IMG = pygame.transform.scale(NUMBER1_IMG, (CELL_WIDTH, CELL_HEIGHT))
    NUMBER2_IMG = pygame.transform.scale(NUMBER2_IMG, (CELL_WIDTH, CELL_HEIGHT))
    NUMBER3_IMG = pygame.transform.scale(NUMBER3_IMG, (CELL_WIDTH, CELL_HEIGHT))
    NUMBER4_IMG = pygame.transform.scale(NUMBER4_IMG, (CELL_WIDTH, CELL_HEIGHT))
    NUMBER5_IMG = pygame.transform.scale(NUMBER5_IMG, (CELL_WIDTH, CELL_HEIGHT))
    NUMBER6_IMG = pygame.transform.scale(NUMBER6_IMG, (CELL_WIDTH, CELL_HEIGHT))
    NUMBER7_IMG = pygame.transform.scale(NUMBER7_IMG, (CELL_WIDTH, CELL_HEIGHT))
    NUMBER8_IMG = pygame.transform.scale(NUMBER8_IMG, (CELL_WIDTH, CELL_HEIGHT))
    NUMBER9_IMG = pygame.transform.scale(NUMBER9_IMG, (CELL_WIDTH, CELL_HEIGHT))
frames = []


# DRAW METHOD
def draw_cell_no_delay(x, y, IMG):
    drawX = X_OFFSET + y * CELL_WIDTH
    drawY = Y_OFFSET + x * CELL_HEIGHT
    WIN.blit(IMG, (drawX, drawY))


def draw_cell(x, y, IMG):
    drawX = X_OFFSET + y * CELL_WIDTH
    drawY = Y_OFFSET + x * CELL_HEIGHT
    WIN.blit(IMG, (drawX, drawY))
    pygame.display.update()
    pygame.time.delay(DELAY)
    pygame_screenshot = pygame.surfarray.array3d(pygame.display.get_surface())
    bgr_frame = cv2.cvtColor(pygame_screenshot, cv2.COLOR_RGB2BGR)
    frames.append(bgr_frame)


def draw_maze(maze_data, rows, cols):
    for row in range(rows):
        for col in range(cols):
            cell = maze_data[row][col]
            if cell == 'x':
                draw_cell_no_delay(row, col, WALL_IMG)
            elif cell == 'S':
                draw_cell_no_delay(row, col, START_IMG)
            elif cell == 'E': # end point
                draw_cell_no_delay(row, col, END_IMG)
            elif cell == 'o':
                draw_cell_no_delay(row, col, TELEPORT_IN_IMG)
            elif cell == 'O': # end point
                draw_cell_no_delay(row, col, TELEPORT_OUT_IMG)
            elif cell == '0' or cell == ' ':
                draw_cell_no_delay(row, col, NUMBER0_IMG)
            elif cell == '1': 
                draw_cell_no_delay(row, col, NUMBER1_IMG)
            elif cell == '2':
                draw_cell_no_delay(row, col, NUMBER2_IMG)
            elif cell == '3':
                draw_cell_no_delay(row, col, NUMBER3_IMG)
            elif cell == '4':
                draw_cell_no_delay(row, col, NUMBER4_IMG)
            elif cell == '5':
                draw_cell_no_delay(row, col, NUMBER5_IMG)
            elif cell == '6':
                draw_cell_no_delay(row, col, NUMBER6_IMG)
            elif cell == '7':
                draw_cell_no_delay(row, col, NUMBER7_IMG)
            elif cell == '8':
                draw_cell_no_delay(row, col, NUMBER8_IMG)
            elif cell == '9':
                draw_cell_no_delay(row, col, NUMBER9_IMG)
                
    pygame_screenshot = pygame.surfarray.array3d(pygame.display.get_surface())
    bgr_frame = cv2.cvtColor(pygame_screenshot, cv2.COLOR_RGB2BGR)
    frames.append(bgr_frame)


# LOAD MAZE GIVEN PATH
def load_maze(maze_path):
    # Set caption
    map_number = int(maze_path.split('/')[-1].replace('input', '').split('.')[0])
    cur_caption = pygame.display.get_caption()[0]
    new_caption = f"{cur_caption} - Map {map_number}"
    pygame.display.set_caption(new_caption)

    # Read maze
    maze_data = []
    gift_data = []
    with open(maze_path, 'r') as file:
        lines = file.read().splitlines()

        n = list(map(int, lines[0].split()))[0]
        for i in range(1, n + 1):
            gift_data.append(list(map(int, lines[i].split())))

        for line in lines[n + 1:]:
            maze_data.append(list(line))

        rows = len(lines) - n - 1
        cols = len(lines[n + 1])

    # Set up sizes and position
    global CELL_WIDTH, CELL_HEIGHT
    if WIDTH / cols < HEIGHT / rows:
        CELL_WIDTH = CELL_HEIGHT = WIDTH / (cols + 2)
    else:
        CELL_WIDTH = CELL_HEIGHT = HEIGHT / (rows + 2)

    global X_OFFSET, Y_OFFSET
    X_OFFSET = (WIDTH - cols * CELL_WIDTH) // 2
    Y_OFFSET = (HEIGHT - rows * CELL_HEIGHT) // 2

    scale_img(CELL_WIDTH, CELL_HEIGHT)

    # Draw maze
    WIN.fill(WHITE)
    draw_maze(maze_data, rows, cols)
    pygame.display.update()
    pygame.time.delay(LONGDELAY)

    return maze_data, gift_data, rows, cols
