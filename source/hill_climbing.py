import sys
import random
from WriteOutput import *
import visualizer
from visualizer import frames, draw_cell, load_maze, dx, dy, WIN, LONGDELAY
import pygame

pygame.display.set_caption("Hill-Climbing Search")

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

def hill_climbing(grid, num_row, num_col):
    start = find_start(grid, num_row, num_col)
    ends = find_ends(grid, num_row, num_col)
    
    if len(ends) < 2:
        print("Not enough endpoints found.")
        return [], []

    def heuristic(x, y, end):
        return abs(x - end[0]) + abs(y - end[1])

    def get_neighbors(x, y):
        neighbors = []
        for i in range(4):
            newX = x + dx[i]
            newY = y + dy[i]
            if 0 <= newX < num_row and 0 <= newY < num_col and grid[newX][newY] != 'x':
                neighbors.append((newX, newY))
        return neighbors

    def hill_climb(start, end):
        current = start
        path = [current]
        while current != end:
            neighbors = get_neighbors(current[0], current[1])
            next_move = max(neighbors, key=lambda n: -heuristic(n[0], n[1], end))
            if heuristic(next_move[0], next_move[1], end) >= heuristic(current[0], current[1], end):
                break
            current = next_move
            path.append(current)
            draw_cell(current[0], current[1], visualizer.VISITED_IMG)
        return path if current == end else []

    path1 = hill_climb(start, ends[0])
    path2 = hill_climb(start, ends[1])

    return path1, path2

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
    paths = hill_climbing(maze_data, rows, cols)
    if paths:
        draw_path(paths[0])
        draw_path(paths[1])

        dir_name = generate_output_path(maze_path, "hill_climbing")
        cost_file = dir_name + "/hill_climbing.txt"
        writeToFile(cost_file, paths, WIN=WIN, frames=frames)
    else:
        print("No path found.")

    # --------------------------------

    pygame.quit()

if len(sys.argv) != 2:
    print("Usage: python hill_climbing.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)
