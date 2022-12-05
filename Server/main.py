import asyncio
import http
import signal
import websockets

from server import Server

if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(Server.startServer())
    event_loop.run_forever()
   
