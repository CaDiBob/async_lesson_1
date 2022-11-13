import os


def get_frames():
    folder = os.path.join('files', 'frames')
    with open(os.path.join(folder, 'rocket_frame_1.txt'))as file:
        rocket_frame_1 = file.read()
    with open(os.path.join(folder, 'rocket_frame_2.txt'))as file:
        rocket_frame_2 = file.read()
    return rocket_frame_1, rocket_frame_2