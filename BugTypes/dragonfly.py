import random

import helper
from .fly import Fly

class DragonFly(Fly):
    colour = "blue"
    strength = 4
    digestion = 5
    birthenergy = 30
    followfood = True
    #         Land Fly
    landchance=[25,75]
    hostility=[100,0]
    flybonus = 4

    def energyloss(self):
        if self.fly:
            self.energy -= ((.03*self.strength) + (.04*self.lastx)**2 + (.04*self.lasty)**2 + (.03*self.flybonus) + (.1*self.digestion)**3)
        else:
            self.energy -= ((.03*self.strength) + (.08*self.lastx)**2 + (.08*self.lasty)**2 + (.1*self.digestion)**3)
        if self.energy <= 0:
            self.die()

    def attack(self, bug):
        if not (not self.fly and hasattr(bug, 'fly') and bug.fly):
            if not (self.classfriendly and issubclass(bug.__class__, self.__class__)) and bug.immunity == 0:
                actualstr = self.strength - self.strdebuff
                enemystr = bug.strength - bug.strdebuff
                if actualstr > enemystr:
                    self.energy += bug.energy
                    self.strdebuff += .5*enemystr
                    helper.killbug(bug)
                elif enemystr < actualstr:
                    bug.energy += self.energy
                    bug.strdebuff += .5*actualstr
                    helper.killbug(self)
                elif self.energy > bug.energy:
                    self.energy -= 0.5*bug.energy
                    helper.killbug(bug)
                elif bug.energy > self.energy:
                    bug.energy -= 0.5*self.energy
                    helper.killbug(self)
            if self.strdebuff > 0:
                self.strdebuff -= .25*self.strength
                if self.strdebuff < 0:
                    self.strdebuff = 0
