import os

INPUT_ROOT = "../input/"


def main():
    solve(INPUT_ROOT + "level_1/")

def solve(prob_path):
    for f in os.listdir(prob_path):
        file_path = os.path.join(prob_path, f)
        if os.path.isfile(file_path):
            if "level_1" in prob_path:
                os.system(f"python bfs_teleportation.py {file_path}")
                os.system(f"python dfs_teleportation.py {file_path}")
                #os.system(f"python astar_heuristic1.py {file_path}")
                #os.system(f"python hill_climbing.py {file_path}")
                #os.system(f"python simulated_annealing.py {file_path}")
                #os.system(f"python dfs.py {file_path}")

if __name__ == "__main__":
    main()
