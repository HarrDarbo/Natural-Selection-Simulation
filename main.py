import helper as glb

from BugTypes.bugnaive import Bug
from BugTypes.buggrounded import BugGround
from food import Food

from canvas import *

import time

def start():
    #spawn initial bugs
    for n in range(20):
        glb.bugs.append(BugGround(n*15,n*15))
    glb.canvas = HCanvas()

    skipr = 0

    while True:
        skipr += 1
        for bug in glb.bugs:
            bug.step()
        for n in range(8):
            glb.makefood()
        glb.canvas.step()
        #time.sleep(0.01)
        if skipr == 1000:
            glb.statistics()
            skipr = 0
        if(len(glb.bugs) == 0):
            print("EVERYBODY DIED!")
            sys.exit(0)

# Get 'er started
if __name__ == "__main__":
    print("\033[1;37;40mStarting Program...")
    glb.init()
    start()
