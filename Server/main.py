import asyncio
import http
import signal
import websockets

from server import Server

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    await Server.startServer()

if __name__ == '__main__':
    asyncio.run(main())
   
