import helper
from .bugnaive import Bug

class WorkerAnt(Bug):
    digestion = 6
    strength = 0.8
    colour = "grey"
    classfriendly = True
    jump = False
    followfood = True
    Queen = None
    childhood = 5

    def __init__(self, x, y, Queen=None, **kwargs):
        super().__init__(x, y, **kwargs)
        if Queen:
            self.Queen = Queen

    def attack(self, bug):
        if bug != self.Queen:
            super().attack(bug)

    def eat(self):
        foodgain = 0
        sign = lambda a: 1 if a>0 else -1
        if self.lastx != 0:
            for n in range(int(abs(self.lastx)+0.5)):
                foodgain += helper.eatfood(int(self.x+.5)-((n*sign(self.lastx))+1), int(self.y+.5)-1) * self.digestion
        if self.lasty != 0:
            for n in range(int(abs(self.lasty)+0.5)):
                foodgain += helper.eatfood(int(self.x+.5)-1, int(self.y+.5)-((n*sign(self.lasty))+1)) * self.digestion
        self.energy += 0.6*foodgain
        if self.Queen:
            self.Queen.energy += 0.4*foodgain
        else:
            self.energy += 0.4*foodgain
        if self.followfood and foodgain > 0:
            self.ate = True
