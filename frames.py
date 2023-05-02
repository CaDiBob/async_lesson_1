import os


def get_rocket_frames():
    frames = []
    folder = os.path.join('files', 'frames')
    files = sorted(os.listdir(folder))
    for frame in files:
        with open(os.path.join(folder, frame))as file:
            rocket_frame = file.read()
        frames.extend([rocket_frame, rocket_frame])
    return frames


def get_garbage_frame():
    frames = []
    folder = os.path.join('files', 'trash')
    files = sorted(os.listdir(folder))
    for frame in files:
        with open(os.path.join(folder, frame))as file:
            garbage_frame = file.read()
        frames.append(garbage_frame)
    return frames
