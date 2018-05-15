import asyncio
import random
import pickle
import bz2

from .constants import REMOTEBOT_PORT

class RobotMonitorProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()

    def datagram_received(self, data, addr):
        message = pickle.loads(bz2.decompress(data))
        print("Receiving from " + addr[0] + ":", message)

def monitor(bind='0.0.0.0', port=REMOTEBOT_PORT):
    loop = asyncio.get_event_loop()
    print("Starting robot monitor")
    protocol = RobotMonitorProtocol()
    coro = loop.create_datagram_endpoint(lambda: protocol, local_addr=(bind, port))
    transport, _ = loop.run_until_complete(coro)
    print("Robot monitor running")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print("Shutting down robot monitor")
    transport.close()
    loop.close()

if __name__ == "__main__":
    monitor()


