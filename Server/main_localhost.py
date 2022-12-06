import asyncio
import websockets
from server import Server

async def startServer():
    await websockets.serve(Server.newPlayerConnected, "localhost", 12345)

if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(startServer())
    event_loop.run_forever()
