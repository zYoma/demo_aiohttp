import websockets # pip install websockets
import asyncio
import time


async def test_url(url, data=""):
    await asyncio.sleep(1)
    async with websockets.connect(url) as websocket:
        await websocket.send(data)
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(*[test_url(f"ws://10.130.0.33:1234/ws/Tester-{n}", "это тест") for n,i in enumerate(range(100))])

if __name__ == "__main__":
    asyncio.run(main())