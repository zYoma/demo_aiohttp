import argparse
import asyncio
import uvloop  # pip install uvloop
import aiohttp

from demo import create_app
from demo.settings import load_conf


# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

parser = argparse.ArgumentParser(description="Demo project")
parser.add_argument('--host', help='Хост', default='10.130.0.33')
parser.add_argument('--port', help='Порт', default=1234)
parser.add_argument('--reload', action='store_true', help='Автоперезапуск')
parser.add_argument(
    '-c', '--config', type=argparse.FileType('r'), help='Путь к файлу конфига')
args = parser.parse_args()

app = create_app(config=load_conf(args.config))

if args.reload:
    print('Поддержка перезапуска активна')
    import aioreloader  # pip install aioreloader
    aioreloader.start()

if __name__ == '__main__':
    aiohttp.web.run_app(app, host=args.host, port=args.port)
