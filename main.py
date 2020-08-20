import helper as glb

from BugTypes import *
from food import Food

from canvas import *

import time
import random


def start():
    # Canvas Creation
    glb.canvas = HCanvas()

    skipr = 0
    timer = 0

    # Main Loop
    time.sleep(0.3)
    timer = time.time()
    while True:
        while glb.Freeze:
            glb.canvas.step()
        skipr += 1
        helper.allstep()
        for n in range(glb.foodspawn):
            glb.makerandomfood()
        glb.canvas.step()
        while(time.time() - timer < .016):
            pass
        timer = time.time()
        #if skipr % 60 == 0:
        #    glb.statistics([GrowBug])
        if skipr % glb.bugspawntimer == 0:
            glb.spawnbugs(glb.bugspawn)

# Get 'er started
if __name__ == "__main__":
    print("\033[1;37;40mStarting Program...")
    glb.init()
    start()
