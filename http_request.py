import asyncio
import aiohttp
from bs4 import BeautifulSoup


def soup(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('title').text.strip()
    return title


async def task(name, work_queue):
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            print(f"{name} URL: {url}")

            async with session.get(url) as response:
                html = await response.read()
            print(f"{name} выполнена")
            print(soup(html))


async def main():
    """
    This is the main entry point for the program.
    """
    # Create the queue of 'work'
    work_queue = asyncio.Queue()
    # Put some 'work' in the queue
    for url in [
        "http://google.com",
        "http://yahoo.com",
        "http://linkedin.com",
        "http://apple.com",
        "http://microsoft.com",
        "http://facebook.com",

    ]:
        await work_queue.put(url)
    # Run the tasks

    await asyncio.gather(
        asyncio.create_task(task('Задача-1', work_queue)),
        asyncio.create_task(task('Задача-2', work_queue)),
    )


if __name__ == "__main__":
    asyncio.run(main())
