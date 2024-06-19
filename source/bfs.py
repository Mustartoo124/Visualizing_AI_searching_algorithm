from collections import deque
from WriteOutput import *
import visualizer
from visualizer import frames,draw_cell, load_maze, dx, dy, WIN, LONGDELAY
import sys

pygame.display.set_caption("BFS")

# --- WRITE GRAPH FUNCTION HERE ---
# You can call function draw_cell(x, y, IMG) to draw IMG at cell (x, y)
def isGoalState(goal1_x, goal1_y, goal2_x, goal2_y, visited):
    if visited[goal1_x][goal1_y] and visited[goal2_x][goal2_y]:
        return True
    return False

def bfs(grid, rows, cols):
    start_x, start_y = None, None

    goal1_x, goal1_y = None, None
    goal2_x, goal2_y = None, None
    count = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 'S':
                start_x, start_y = i, j
            elif grid[i][j] == 'E' and count == 0:
                goal1_x, goal1_y = i, j
                count += 1
            elif grid[i][j] == 'E' and count == 1:
                goal2_x, goal2_y = i, j


    visited = [[False for _ in range(cols)] for _ in range(rows)]
    trace = [[(0, 0) for _ in range(cols)] for _ in range(rows)]
    queue = deque()

    queue.append((start_x, start_y))
    visited[start_x][start_y] = True

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
                queue.append((new_x, new_y))
                visited[new_x][new_y] = True
                trace[new_x][new_y] = (x, y)

                """ goal1Checked = False 
                    goal1 = []
                    goal2 = []
                    if new_x == 0 or new_x == rows - 1 or new_y == 0 or new_y == cols - 1: # check end point 
                        if (goal1Checked == False): 
                            while new_x != start_x or new_y != start_y:
                                goal1.append((new_x, new_y))
                                new_x, new_y = trace[new_x][new_y]
                            goal1.append((start_x, start_y))
                            goal1.reverse()
                        else: 
                            while new_x != start_x or new_y != start_y:
                                goal1.append((new_x, new_y))
                                new_x, new_y = trace[new_x][new_y]
                            goal1.append((start_x, start_y))
                            goal1.reverse()
                        return goal1, goal2  """
                
                if isGoalState(goal1_x, goal1_y, goal2_x, goal2_y, visited):
                    path1 = []
                    path2 = []
                    new_x, new_y = goal1_x, goal1_y
                    while new_x != start_x or new_y != start_y:
                        path1.append((new_x, new_y))
                        new_x, new_y = trace[new_x][new_y]
                    path1.append((start_x, start_y))
                    path1.reverse()

                    new_x, new_y = goal2_x, goal2_y
                    while new_x != start_x or new_y != start_y:
                        path2.append((new_x, new_y))
                        new_x, new_y = trace[new_x][new_y]
                    path2.append((start_x, start_y))
                    path2.reverse()
                    return path1, path2
                draw_cell(new_x, new_y, visualizer.VISITED_IMG)
    return []

def draw_path(path):
    if len(path) == 0: 
        return

    pygame.time.delay(LONGDELAY)
    draw_cell(path[0][0], path[0][1], visualizer.START_CHECK_IMG)
    end = path[-1]
    path = path[1:-1]
    for x, y in path:
        draw_cell(x, y, visualizer.PATH_IMG)
    draw_cell(end[0], end[1], visualizer.DOOR_OPEN)
# ---------------------------------

def main(maze_path):
    maze_data, gift_data, rows, cols = load_maze(maze_path)

    # --- CALL GRAPH FUNCTION HERE ---
    # Ex: DFS(maze_data, gift_data, rows, cols)
    path = bfs(maze_data, rows, cols)
    draw_path(path[0])
    draw_path(path[1]) 

    dir_name = generate_output_path(maze_path, "bfs")
    cost_file = dir_name + "/bfs.txt"
    writeToFile(cost_file, path, WIN=WIN, frames=frames)

    # --------------------------------
    pygame.quit()

if len(sys.argv) != 2:
    print("Usage: python bfs.py <path>")
    maze_path = "../input/level_1/input3.txt"
    main(maze_path)
else:
    maze_path = sys.argv[1]
    main(maze_path)
