import remotebot

def my_routine():
    import time
    import os
    import random
    echo("starting")
    rand = random.random()
    while True:
        echo(rand)
        time.sleep(2)

remotebot.send(my_routine, "192.168.1.109")
