import time
import curses
import asyncio
import random


TIC_TIMEOUT = 0.1


async def blink(canvas, row, column, symbol):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(1 * 20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(1 * 3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(1 * 5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(1 * 3):
            await asyncio.sleep(0)


def get_star():
    stars = [
        '+', '*', '.', ':'
    ]
    star = random.choice(stars)
    return star


def get_place_on_canvas(y, x):
    row = random.randint(2, y)
    column = random.randint(2, x)
    return row, column



def draw(canvas):
    y, x = canvas.getmaxyx()
    canvas.border()
    coroutines = []
    for _ in range(16):
        coroutines.append(
            blink(canvas, *get_place_on_canvas(y, x), get_star())
        )
    while True:
        for coroutine in coroutines:
            coroutine.send(None)
        curses.curs_set(False)
        time.sleep(TIC_TIMEOUT)
        canvas.refresh()


def main():
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == '__main__':
    main()
