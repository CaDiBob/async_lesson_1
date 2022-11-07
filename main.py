import time
import curses
import asyncio
import random

from itertools import cycle

from frames import get_frames
from curses_tools import draw_frame


TIC_TIMEOUT = 0.1


async def animate_spaceship(canvas, start_row, start_column, frames):
    for frame in cycle(frames):
        draw_frame(canvas, start_row, start_column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, start_row, start_column, frame, negative=True)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def get_timeout(seconds):
    iterations = int(seconds)
    for _ in range(iterations):
        await asyncio.sleep(0)


async def blink(
        canvas, row, column, symbol, state_1, state_2, state_3, state_4):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await get_timeout(state_1)

        canvas.addstr(row, column, symbol)
        await get_timeout(state_2)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await get_timeout(state_3)

        canvas.addstr(row, column, symbol)
        await get_timeout(state_4)


def get_star():
    stars = [
        '+', '*', '.', ':'
    ]
    star = random.choice(stars)
    return star


def get_place_on_canvas(y, x):
    row = random.randint(2, y)
    column = random.randint(1, x)
    return row, column


def get_coroutines(canvas, y, x):
    coroutines = []
    for coroutine in range(14):
        coroutine = blink(
            canvas,
            *get_place_on_canvas(y, x),
            get_star(),
            state_1=random.randint(3, 6),
            state_2=random.randint(5, 10),
            state_3=random.randint(6, 13),
            state_4=random.randint(6, 13),
        )
        coroutines.append(coroutine)
    return coroutines


def get_center_on_canvas(y, x):
    start_row = y / 2
    start_column = x / 2
    return start_row, start_column


def draw(canvas):
    frames = get_frames()
    y, x = canvas.getmaxyx()
    canvas.border()
    coroutines = get_coroutines(canvas, y, x)
    start_row_centre, start_column_centre = get_center_on_canvas(y, x)
    shot = fire(
        canvas,
        start_row_centre,
        start_column_centre,
        rows_speed=-0.3,
        columns_speed=0
    )
    frame = animate_spaceship(
        canvas,
        start_row_centre,
        start_column_centre,
        frames,
    )
    coroutines.append(shot)
    coroutines.append(frame)
    while True:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        curses.curs_set(False)
        time.sleep(TIC_TIMEOUT)
        canvas.refresh()


def main():
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == '__main__':
    main()
