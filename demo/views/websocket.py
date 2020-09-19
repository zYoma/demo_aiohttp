import json

from aiohttp import web, WSMsgType


class WebSocket(web.View):

    async def get(self):
        self.user = self.request.match_info['user']
        app = self.request.app

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        app.wslist[self.user] = ws
        await self.broadcast({'text': 'подключился', 'user': self.user})

        async for msg in ws:
            if msg.type == WSMsgType.text:
                if msg.data == 'close':
                    await ws.close()
                else:
                    text = msg.data.strip()
                    await self.broadcast({'text': f'{text}', 'user': self.user})

            elif msg.type == WSMsgType.error:
                print(f'Ошибка {ws.exception()}')

        await self.disconnect(self.user, ws)
        return ws

    # async def command(self, cmd):
    #     """ Run chat command """
    #     app = self.request.app

    #     if cmd.startswith('/kill'):
    #         pass
    #     else:
    #         return {'text': f'{cmd}', 'user':self.user}

    async def broadcast(self, message):
        """ Отправка сообщений всем. """
        for peer in self.request.app.wslist.values():
            await peer.send_json(message)

    async def disconnect(self, user, socket, silent=False):
        """ Закрываем соединение и отправлем сообщение о выходе. """
        app = self.request.app
        app.wslist.pop(user, None)
        if not socket.closed:
            await socket.close()
        if silent:
            return

        await self.broadcast({'text': 'Вышел из чата', 'user': self.user})
