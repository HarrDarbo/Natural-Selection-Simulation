import helper as glb

from bug import Bug
from food import Food

from canvas import *

import time

def start():
    for n in range(20):
        glb.bugs.append(Bug(n*15,n*15))
    for n in range(100):
        glb.foods.append(Food())
    glb.canvas = HCanvas()

    while True:
        for bug in glb.bugs:
            bug.step()
        for n in range(8):
            glb.makefood()
        glb.canvas.step()
        time.sleep(0.01)
        if(len(glb.bugs) == 0):
            print("EVERYBODY DIED!")
            sys.exit(0)

# Get 'er started
if __name__ == "__main__":
    print("\033[1;37;40mStarting Program...")
    glb.init()
    start()
