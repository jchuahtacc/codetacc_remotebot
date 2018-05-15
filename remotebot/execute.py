import socket
import bz2
import asyncio
import marshal
import pickle

from .constants import REMOTEBOT_PORT

def run_motor(motornum, speed, direction):
    pass

def echo(message, ip=None, port=None):
    if not ip and echo.__ip__:
        ip = echo.__ip__
    if not port and echo.__port__:
        port = echo.__port__
    print("Sending to " + ip + ":", message)
    dgram = bz2.compress(pickle.dumps(message))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(dgram, (ip, port))

async def tcp_send(data, ip, port, loop):
    print("Sending to", ip)
    reader, writer = await asyncio.open_connection(ip, port, loop=loop)
    writer.write(data)
    writer.close()

def send(routine, ip, port=REMOTEBOT_PORT, monitor_ip=None, monitor_port=REMOTEBOT_PORT, inference_ip=None, inference_port=REMOTEBOT_PORT):
    payload = { "monitor_ip" : monitor_ip, "monitor_port" : monitor_port,
             "inference_ip" : inference_ip, "inference_port" : inference_port,
             "code" : routine.__code__ }
    data = bz2.compress(marshal.dumps(payload))
    try:
        loop
    except NameError:
        loop = asyncio.get_event_loop()
    else:
        if loop and loop.is_closed():
            loop = asyncio.new_event_loop()
    loop.run_until_complete(tcp_send(data, ip, port, loop))
    #loop.close()
