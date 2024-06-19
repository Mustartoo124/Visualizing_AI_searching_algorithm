import sys
import heapq
from WriteOutput import *
import visualizer
from visualizer import frames, draw_cell, load_maze, dx, dy, WIN, LONGDELAY
import pygame

pygame.display.set_caption("A* - Manhattan distance heuristic")

# --- WRITE GRAPH FUNCTION HERE ---
def find_start(grid, num_row, num_col):
    for i in range(num_row):
        for j in range(num_col):
            if grid[i][j] == 'S':
                return [i, j]

def find_ends(grid, num_row, num_col):
    ends = []
    for i in range(num_row):
        for j in range(num_col):
            if grid[i][j] == 'E':
                ends.append([i, j])
                if len(ends) == 2:
                    return ends
    return ends

def aStar(grid, num_row, num_col):
    start = find_start(grid, num_row, num_col)
    ends = find_ends(grid, num_row, num_col)
    
    if len(ends) < 2:
        print("Not enough endpoints found.")
        return [], []

    MAX_DIS = 1_000_000_000
    distance = [[MAX_DIS for _ in range(num_col)] for _ in range(num_row)]
    trace = [[[-1, -1] for _ in range(num_col)] for _ in range(num_row)]
    open_list = [[False for _ in range(num_col)] for _ in range(num_row)]
    heap = []  # this is for getting min f = g + h

    def h(x, y, end):
        return abs(x - end[0]) + abs(y - end[1])

    def constructPath(end):
        X, Y = end
        path = []
        while [X, Y] != [-1, -1]:
            path.append([X, Y])
            X, Y = trace[X][Y]
        path.reverse()
        return path

    def inGrid(x, y):
        return 0 <= x < num_row and 0 <= y < num_col

    distance[start[0]][start[1]] = 0
    for end in ends:
        heapq.heappush(heap, [h(start[0], start[1], end), start])
    open_list[start[0]][start[1]] = True

    found_paths = []
    found_ends = []

    while heap and len(found_ends) < 2:
        cur = heapq.heappop(heap)
        cur_cell = cur[1]

        if cur_cell in ends and cur_cell not in found_ends:
            found_ends.append(cur_cell)
            found_paths.append(constructPath(cur_cell))
            if len(found_ends) == 2:
                return found_paths
            continue

        if cur_cell != start:
            draw_cell(cur_cell[0], cur_cell[1], visualizer.VISITED_IMG)

        open_list[cur_cell[0]][cur_cell[1]] = False
        for i in range(4):
            newX = cur_cell[0] + dx[i]
            newY = cur_cell[1] + dy[i]

            if not inGrid(newX, newY) or grid[newX][newY] == 'x':
                continue

            # Read the weight from the grid
            cell_weight = int(grid[newX][newY]) if grid[newX][newY] != 'S' and grid[newX][newY] != 'E' else 1
            proposal_gScore = distance[cur_cell[0]][cur_cell[1]] + cell_weight
            if proposal_gScore < distance[newX][newY]:
                distance[newX][newY] = proposal_gScore
                fScore = proposal_gScore + h(newX, newY, ends[0])  # Use the first end as the heuristic target
                trace[newX][newY] = cur_cell
                if not open_list[newX][newY]:
                    heapq.heappush(heap, [fScore, [newX, newY]])
                    open_list[newX][newY] = True

    return found_paths if len(found_paths) == 2 else (found_paths, [])

def draw_path(path):
    if not path:
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
    paths = aStar(maze_data, rows, cols)
    if paths and len(paths) == 2:
        draw_path(paths[0])
        draw_path(paths[1])

        dir_name = generate_output_path(maze_path, "astar_heuristic_1")
        cost_file = dir_name + "/astar_heuristic_1.txt"
        writeToFile(cost_file, paths, WIN=WIN, frames=frames)
    else:
        print("No path found.")

    # --------------------------------

    pygame.quit()

if len(sys.argv) != 2:
    print("Usage: python astar_heuristic1.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)
