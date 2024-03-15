import sys
import time
import curses
import asyncio
import random

from itertools import cycle

from frames import get_rocket_frames, get_garbage_frames
from physics import update_speed
from curses_tools import (
    draw_frame,
    read_controls,
    get_frame_size
)


TIC_TIMEOUT = 0.1


async def fill_orbit_with_garbage(canvas):
    *_, width = get_size_free_space(canvas)
    garbage_frames = get_garbage_frames()
    while True:
        trash = fly_garbage(
            canvas,
            random.randint(2, width-2),
            random.choice(garbage_frames),
        )
        await sleep(10)
        coroutines.append(trash)
        await sleep(10)


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def animate_spaceship(canvas, row, column, height, width, frames):
    frame, *_ = frames
    frame_width, frame_height = get_frame_size(frame)
    height -= frame_height
    width -= frame_width
    row_speed = column_speed = 0
    for frame in cycle(frames):
        rows_direction, columns_direction, _ = read_controls(canvas)
        row_speed, column_speed = update_speed(row_speed, column_speed, rows_direction, columns_direction)
        if rows_direction or columns_direction:
            row += row_speed
            column += column_speed
            row = max(2, row)
            column = max(2, column)

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


async def sleep(tics=1):
    iterations = int(tics)
    for _ in range(iterations):
        await asyncio.sleep(0)


async def blink(
        canvas, row, column, symbol, state_1, state_2, state_3, state_4):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(state_1)

        canvas.addstr(row, column, symbol)
        await sleep(state_2)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(state_3)

        canvas.addstr(row, column, symbol)
        await sleep(state_4)


def get_size_free_space(canvas):
    border = 5
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
    global coroutines
    frames = get_rocket_frames()
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
    garbage = fill_orbit_with_garbage(canvas)
    coroutines.append(garbage)
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
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
