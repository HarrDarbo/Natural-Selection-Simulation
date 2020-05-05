import helper as glb

from BugTypes import *
from food import Food

from canvas import *

import time

def spawnall(amt):
    for n in range(amt):
        glb.makebug(Bug(n*15, n*15))
        glb.makebug(BugGround(n*15, glb.clen-(n*15)))
        glb.makebug(Fly(glb.clen-(n*15), n*15))
        glb.makebug(LowFly(glb.clen-(n*15), glb.clen-(n*15)))
        glb.makebug(DragonFly(glb.clen/2, n*15))

def start():
    #spawn initial bugs
    spawnall(15)

    BugSpawns=[Bug.__name__,BugGround.__name__,Fly.__name__,LowFly.__name__,DragonFly.__name__]

    # Canvas Creation
    glb.canvas = HCanvas()

    # Initial Food Sources
    for n in range(8000):
        glb.makefood()

    skipr = 0

    # Main Loop
    while True:
        skipr += 1
        for bug in glb.bugs:
            bug.step()
        for n in range(12):
            glb.makefood()
        glb.canvas.step()
        #time.sleep(0.01)
        if skipr % 100 == 0:
            glb.statistics(BugSpawns)
        #if skipr % 1000 == 0:
            #spawnall(5)
        if(len(glb.bugs) == 0):
            print("EVERYBODY DIED!")
            sys.exit(0)

# Get 'er started
if __name__ == "__main__":
    print("\033[1;37;40mStarting Program...")
    glb.init()
    start()
