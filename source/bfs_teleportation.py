from collections import deque
import sys
import time  # Thêm thư viện time để tính thời gian chạy
from WriteOutput import *
import visualizer
from visualizer import frames, draw_cell, draw_cell_no_delay, load_maze, dx, dy, WIN, LONGDELAY

pygame.display.set_caption("Teleporter: BFS")

def bfs(grid, teleport_data, rows, cols):
    start_time = time.time()  # Ghi lại thời gian bắt đầu
    start_x, start_y = None, None
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 'S':
                start_x, start_y = i, j
                break
        if start_x is not None:
            break
    if start_x is None:
        return [], 0, 0

    visited = [[False for _ in range(cols)] for _ in range(rows)]
    trace = [[(0, 0) for _ in range(cols)] for _ in range(rows)]
    queue = deque()
    visited_count = 0  # Biến đếm số lượng node được thăm

    queue.append((start_x, start_y))
    visited[start_x][start_y] = True
    visited_count += 1

    while queue:
        x, y = queue.popleft()

        for i in range(4):
            new_x, new_y = x + dx[i], y + dy[i]

            if (
                0 <= new_x < rows
                and 0 <= new_y < cols
                and not visited[new_x][new_y]
                and grid[new_x][new_y] != 'x'
            ):
                visited[new_x][new_y] = True
                trace[new_x][new_y] = (x, y)
                visited_count += 1

                if grid[new_x][new_y] == 'o':
                    for teleport in teleport_data:
                        x1, y1, x2, y2 = teleport
                        if (new_x, new_y) == (x1, y1):
                            queue.append((x2, y2))
                            visited[x2][y2] = True
                            trace[x2][y2] = (new_x, new_y)
                            visited_count += 1
                    continue
                queue.append((new_x, new_y))

                if new_x == 15 and new_y == 18:
                    path = []
                    while new_x != start_x or new_y != start_y:
                        path.append((new_x, new_y))
                        new_x, new_y = trace[new_x][new_y]
                    path.append((start_x, start_y))
                    path.reverse()
                    end_time = time.time()  # Ghi lại thời gian kết thúc
                    execution_time = end_time - start_time
                    return path, visited_count, execution_time

                if grid[new_x][new_y] != 'o' and grid[new_x][new_y] != 'O':
                    draw_cell(new_x, new_y, visualizer.VISITED_IMG)

    end_time = time.time()  # Ghi lại thời gian kết thúc
    execution_time = end_time - start_time
    return [], visited_count, execution_time

def draw_path(path, teleport_data):
    if len(path) == 0:
        return
    pygame.time.delay(LONGDELAY)
    draw_cell(path[0][0], path[0][1], visualizer.START_CHECK_IMG)
    end = path[-1]
    path = path[1:-1]
    for x, y in path:
        is_teleport = False
        for teleport in teleport_data:
            x1, y1, x2, y2 = teleport
            if (x, y) == (x1, y1):
                is_teleport = True
                draw_cell(x, y, visualizer.TELEPORT_IN_VISITED_IMG)
                break
            if (x, y) == (x2, y2):
                is_teleport = True
                draw_cell(x, y, visualizer.TELEPORT_OUT_VISITED_IMG)
                break
        if not is_teleport:
            draw_cell(x, y, visualizer.PATH_IMG)
    draw_cell(end[0], end[1], visualizer.DOOR_OPEN)

def main(maze_path):
    maze_data, teleport_data, rows, cols = load_maze(maze_path)
    path, visited_count, execution_time = bfs(maze_data, teleport_data, rows, cols)
    draw_path(path, teleport_data)

    dir_name = generate_output_path(maze_path, "BFS_teleporter")
    cost_file = dir_name + "/teleporter.txt"

    writeToFile(cost_file, path, 0, WIN, frames, visited_count, execution_time)

    pygame.quit()

if len(sys.argv) != 2:
    print("Usage: python bfs_teleportation.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)
