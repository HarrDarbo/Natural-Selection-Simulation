import random
import math

import helper
from .fly import Fly

class LowFly(Fly):
    colour = "orange"
    jump = False
    followfood = False

    def energyloss(self):
        if self.fly:
            self.energy -= ((.5*self.strength) + (.15*self.lastx)**2 + (.15*self.lasty)**2 + (.06*self.flybonus) + (.05*self.digestion)**3)
        else:
            self.energy -= ((.25*self.strength) + (.05*self.lastx)**2 + (.05*self.lasty)**2 + (.04*self.digestion)**3)
        if self.energy <= 0:
            self.die()

    def eat(self):
        self.energy += helper.eatfood(int(self.x+.5)-1, int(self.y+.5)-1) * self.digestion
        if self.energy > 50 + math.log(self.digestion):
            self.energy -= 30
            self.reproduce()
