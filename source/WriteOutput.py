import os
import cv2
import pygame


def writeToFile(file_name="output.txt", path=None, bonus=0, WIN=None, frames=None, visited_count=None, execution_time=None):
    if path is None:
        return

    # Create the directory structure if it doesn't exist
    directory = os.path.dirname(file_name)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(file_name, 'w') as out:
        leng = len(path)
        if leng == 0:
            out.write("NO\n")
        else:
            out.write(f"{leng - 1 + bonus}\n")
        # Ghi visited_count và execution_time vào file
        if visited_count is not None:
            out.write(f"Visited Nodes: {visited_count}\n")
        if execution_time is not None:
            out.write(f"Execution Time: {execution_time:.4f} seconds\n")

    if WIN is None:
        return

    image_path = file_name.split('.txt')[0] + '.jpg'
    pygame.image.save(WIN, image_path)

    video_path = file_name.split('.txt')[0] + '.mp4'
    height, width, layers = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Định dạng video codec
    out = cv2.VideoWriter(video_path, fourcc, 30.0, (height, width))
    rotated_frames = [cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) for frame in frames]
    flipped_frames_horizontal = [cv2.flip(frame, 1) for frame in rotated_frames]
    for frame in flipped_frames_horizontal:
        out.write(frame)
    out.release()

    print(f"-----Saved cost(.txt), path(.jpg) and video(.mp4) at {directory}-----")

def checkDuplicatePointInPath(path):
    s = set()
    for point in path:
        p_tuple = tuple(point)
        if p_tuple in s:
            return True
        s.add(p_tuple)
    return False

def generate_output_path(maze_path, algorithm):
    # Extract the directory of the input maze path
    base_directory = maze_path[:-4]
    tmp = base_directory.split("/")
    tmp = tmp[2:]
    base_directory = "/".join(tmp)

    # Construct the output directory path
    output_directory = os.path.join('..', 'output', base_directory, algorithm)

    # print(output_directory)

    return output_directory


