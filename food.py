import helper
import random

class Food(object):
    x = -1
    y = -1
    def __init__(self):
        self.x = int(random.random()*helper.clen)
        self.y = int(random.random()*helper.clen)
