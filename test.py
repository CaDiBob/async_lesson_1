import asyncio


async def func(num):
    print('Starting func {0}...'.format(num))
    await asyncio.sleep(10)
    print('Ending func {0}...'.format(num))

async def create_tasks_func():
    tasks = list()
    for i in range(5):
        tasks.append(asyncio.create_task(func(i)))
    await asyncio.wait(tasks)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_tasks_func())
    loop.close()


if __name__ == "__main__":
    main()
