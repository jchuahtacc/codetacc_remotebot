import remotebot

def my_routine():
    import time
    import os
    import random
    random.notafunction()
    echo("starting")
    rand = random.random()
    while True:
        echo(rand)
        time.sleep(2)

remotebot.send(my_routine, "10.146.123.122")
