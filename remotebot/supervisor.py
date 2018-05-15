from .execute import *
from .variables import REMOTEBOT_PORT

from multiprocessing import Process
import bz2
import asyncio
import marshal

current_process = None

def __dummy__():
    print("Dummy code, should not see")
    pass

def run_routine(payload):
    try:
        echo.__ip__ = payload["monitor_ip"]
        echo.__port__ = payload["monitor_port"]
        __dummy__.__code__ = payload["code"]
        __dummy__()
    except Exception as e:
        echo(e)

async def handle_routine(reader, writer):
    global current_process
    global __dummy__
    data = await reader.read()
    payload = marshal.loads(bz2.decompress(data))
    # __dummy__.__code__ = marshal.loads(bz2.decompress(data))
    addr = writer.get_extra_info('peername')
    print("Received routine from", addr)
    if not payload["monitor_ip"]:
        payload["monitor_ip"] = addr[0]
    if current_process and current_process.is_alive():
        print("Terminating previous process")
        current_process.terminate()
        run_motor(1, 0, "stop")
        run_motor(2, 0, "stop")
    print("Starting new process")
    current_process = Process(target=run_routine, args=(payload,))
    current_process.start()

def supervisor(bind="0.0.0.0", port=REMOTEBOT_PORT):
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_routine, bind, port, loop=loop)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":
    supervisor()
