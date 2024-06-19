import sys
import random
import math
from WriteOutput import *
import visualizer
from visualizer import frames, draw_cell, load_maze, dx, dy, WIN, LONGDELAY
import pygame

pygame.display.set_caption("Simulated Annealing Search")

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

def simulated_annealing(grid, num_row, num_col, start, end):
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

    def acceptance_probability(old_cost, new_cost, temperature):
        if new_cost < old_cost:
            return 1.0
        return math.exp((old_cost - new_cost) / temperature)

    current = start
    current_cost = heuristic(current[0], current[1], end)
    path = [current]

    initial_temperature = 100.0
    final_temperature = 1.0
    alpha = 0.99
    temperature = initial_temperature

    while temperature > final_temperature:
        neighbors = get_neighbors(current[0], current[1])
        if not neighbors:
            break

        next_move = random.choice(neighbors)
        next_cost = heuristic(next_move[0], next_move[1], end)

        if acceptance_probability(current_cost, next_cost, temperature) > random.random():
            current = next_move
            current_cost = next_cost
            path.append(current)
            draw_cell(current[0], current[1], visualizer.VISITED_IMG)
            if current == end:
                return path

        temperature *= alpha

    return []

def find_paths(grid, num_row, num_col):
    start = find_start(grid, num_row, num_col)
    ends = find_ends(grid, num_row, num_col)
    
    if len(ends) < 2:
        print("Not enough endpoints found.")
        return [], []

    path1 = simulated_annealing(grid, num_row, num_col, start, ends[0])
    path2 = simulated_annealing(grid, num_row, num_col, start, ends[1])

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

        dir_name = generate_output_path(maze_path, "simulated_annealing")
        cost_file = dir_name + "/simulated_annealing.txt"
        writeToFile(cost_file, paths, WIN=WIN, frames=frames)
    else:
        print("No path found.")

    # --------------------------------

    pygame.quit()

if len(sys.argv) != 2:
    print("Usage: python simulated_annealing.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)
