import sys
from WriteOutput import *
import visualizer
from visualizer import frames, draw_cell, load_maze, dx, dy, WIN, LONGDELAY
import pygame

pygame.display.set_caption("DFS Search")

# --- WRITE GRAPH FUNCTION HERE ---
def find_start(grid, num_row, num_col):
    for i in range(num_row):
        for j in range(num_col):
            if grid[i][j] == 'S':
                return (i, j)
    return None

def find_ends(grid, num_row, num_col):
    ends = []
    for i in range(num_row):
        for j in range(num_col):
            if grid[i][j] == 'E':
                ends.append((i, j))
                if len(ends) == 2:
                    return ends
    return ends

def dfs(grid, num_row, num_col, start, end):
    visited = [[False] * num_col for _ in range(num_row)]
    path = []

    def is_valid(x, y):
        return 0 <= x < num_row and 0 <= y < num_col and not visited[x][y] and grid[x][y] != 'x'

    def dfs_helper(x, y):
        nonlocal path
        if (x, y) == end:
            path.append((x, y))
            return True
        if is_valid(x, y):
            visited[x][y] = True
            path.append((x, y))
            for i in range(4):
                new_x, new_y = x + dx[i], y + dy[i]
                if dfs_helper(new_x, new_y):
                    return True
            path.pop()
            visited[x][y] = False
        return False

    if dfs_helper(start[0], start[1]):
        return path
    else:
        return []

def find_paths(grid, num_row, num_col):
    start = find_start(grid, num_row, num_col)
    ends = find_ends(grid, num_row, num_col)
    
    if not start or len(ends) < 2:
        print("Invalid maze configuration.")
        return [], []

    path1 = dfs(grid, num_row, num_col, start, ends[0])
    path2 = dfs(grid, num_row, num_col, start, ends[1])

    return path1, path2

def draw_paths(paths):
    if not paths[0] or not paths[1]:
        return
    pygame.time.delay(LONGDELAY)
    for path in paths:
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
    paths = find_paths(maze_data, rows, cols)
    if paths:
        draw_paths(paths)

        dir_name = generate_output_path(maze_path, "dfs")
        cost_file = dir_name + "/dfs.txt"
        writeToFile(cost_file, paths, WIN=WIN, frames=frames)
    else:
        print("No path found.")

    # --------------------------------

    pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dfs.py <path>")
    else:
        maze_path = sys.argv[1]
        main(maze_path)
