import time
import curses
import asyncio
import random


TIC_TIMEOUT = 0.1


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
    for coroutine in range(15):
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


def draw(canvas):
    y, x = canvas.getmaxyx()
    canvas.border()
    coroutines = get_coroutines(canvas, y, x)
    iter = 0
    while True:
        for coroutine in coroutines:
            coroutine.send(None)
        curses.curs_set(False)
        time.sleep(TIC_TIMEOUT)
        canvas.refresh()
        iter += 1



def main():
    curses.update_lines_cols()
    curses.wrapper(draw)

if __name__ == '__main__':
    main()
