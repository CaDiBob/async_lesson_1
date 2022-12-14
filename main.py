import time
import curses
import asyncio
import random

from itertools import cycle

from frames import get_frames
from curses_tools import (
    draw_frame,
    read_controls,
    get_frame_size
)


TIC_TIMEOUT = 0.1


async def animate_spaceship(canvas, row, column, height, width, frames):
    frame, *_ = frames
    frame_width, frame_height = get_frame_size(frame)
    height -= frame_height
    width -= frame_width
    for frame in cycle(frames):
        rows_direction, columns_direction, _ = read_controls(canvas)
        if rows_direction or columns_direction:
            row += rows_direction
            column += columns_direction
            row = max(1, row)
            column = max(1, column)

            row = min(row, height)
            column = min(column, width)
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)



async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):

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


def get_size_free_space(canvas):
    border = 2
    raw_height, raw_width = canvas.getmaxyx()
    height = raw_height - border
    width = raw_width - border
    return height, width


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


def get_coroutines_for_stars(canvas, y, x):
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
    return round(start_row), round(start_column)


def draw(canvas):
    frames = get_frames()
    height, width = get_size_free_space(canvas)
    canvas.border()
    canvas.nodelay(True)
    coroutines = get_coroutines_for_stars(canvas, height, width)
    start_row_centre, start_column_centre = get_center_on_canvas(height, width)
    spaceship = animate_spaceship(
        canvas,
        start_row_centre,
        start_column_centre,
        height,
        width,
        frames,
    )
    coroutines.append(spaceship)
    while True:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        curses.curs_set(False)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def main():
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == '__main__':
    main()
