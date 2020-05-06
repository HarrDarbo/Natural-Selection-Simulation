import helper as glb

from BugTypes import *
from food import Food

from canvas import *

import time
import random

def spawnall(amt):
    for n in range(amt):
        glb.makebug(Bug(int(random.random()*helper.clen)-1, int(random.random()*helper.clen)-1))
        glb.makebug(Beetle(int(random.random()*helper.clen)-1, int(random.random()*helper.clen)-1))
        glb.makebug(Fly(int(random.random()*helper.clen)-1, int(random.random()*helper.clen)-1))
        glb.makebug(LowFly(int(random.random()*helper.clen)-1, int(random.random()*helper.clen)-1))
        glb.makebug(DragonFly(int(random.random()*helper.clen)-1, int(random.random()*helper.clen)-1))
        glb.makebug(Tick(int(random.random()*helper.clen)-1, int(random.random()*helper.clen)-1))

def spawnants(amt):
    for n in range(amt):
        glb.makebug(QueenAnt(int(random.random()*helper.clen)-1, int(random.random()*helper.clen)-1))

def start():
    #spawn initial bugs
    spawnall(15)
    spawnants(1)


    BugSpawns=[Bug.__name__,Beetle.__name__,Fly.__name__,LowFly.__name__,DragonFly.__name__,QueenAnt.__name__,WorkerAnt.__name__,Tick.__name__]

    # Canvas Creation
    glb.canvas = HCanvas()

    # Initial Food Sources
    for n in range(8000):
        glb.makefood()

    skipr = 0

    # Main Loop
    time.sleep(0.5)
    while True:
        skipr += 1
        for bug in glb.bugs:
            bug.step()
        for n in range(int(((glb.clen/10)**2)/50)):
            glb.makefood()
        glb.canvas.step()
        #time.sleep(0.01)
        if skipr % 100 == 0:
            glb.statistics(BugSpawns)
        if skipr % 100 == 0:
            spawnall(1)
        if skipr % 2000 == 0:
            spawnants(1)
        if(len(glb.bugs) == 0):
            print("EVERYBODY DIED!")
            sys.exit(0)

# Get 'er started
if __name__ == "__main__":
    print("\033[1;37;40mStarting Program...")
    glb.init()
    start()
