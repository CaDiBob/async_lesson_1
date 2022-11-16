import os


def get_frames():
    frames = []
    folder = os.path.join('files', 'frames')
    files = sorted(os.listdir(folder))
    for frame in files:
        with open(os.path.join(folder, frame))as file:
            rocket_frame = file.read()
        frames.append(rocket_frame)
    return frames
