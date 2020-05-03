import helper
import random

class Food(object):
    x = -1
    y = -1
    def __init__(self):
        self.x = random.random()*helper.clen
        self.y = random.random()*helper.clen
