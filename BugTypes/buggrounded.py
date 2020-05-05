import helper
from .bugnaive import Bug

class BugGround(Bug):
    digestion = 9
    colour = "magenta"
    classfriendly = True
    jump = False
    followfood = True
    def eat(self):
        sign = lambda a: 1 if a>0 else -1
        if self.lastx != 0:
            for n in range(int(abs(self.lastx)+0.5)):
                self.energy += helper.eatfood(int(self.x+.5)-((n*sign(self.lastx))+1), int(self.y+.5)-1) * self.digestion
        if self.lasty != 0:
            for n in range(int(abs(self.lasty)+0.5)):
                self.energy += helper.eatfood(int(self.x+.5)-1, int(self.y+.5)-((n*sign(self.lasty))+1)) * self.digestion

        if self.energy > 50:
            self.energy -= self.birthenergy
            self.reproduce()
