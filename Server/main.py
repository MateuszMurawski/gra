import asyncio
import http
import signal
import websockets

from server import Server

async def health_check(path, request_headers):
    if path == "/healthz":
        return http.HTTPStatus.OK, [], b"OK\n"

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        Server.newPlayerConnected,
        host="",
        port=6666,
        process_request=health_check,
    ):
        await stop
        

if __name__ == '__main__':
    asyncio.run(main())
   
