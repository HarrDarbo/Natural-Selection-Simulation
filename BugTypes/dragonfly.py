import random

import helper
from .fly import Fly

class DragonFly(Fly):
    colour = "blue"
    strength = 5
    digestion = 4
    classfriendly = True
    #         Land Fly
    landchance=[25,75]
    hostility=[100,1]
    flybonus = 3
    sight = 10
    patience = 50
    sightbonus = 10

    def energyloss(self):
        if self.fly:
            self.energy -= ((.1*self.strength) + (.02*self.lastx)**3 + (.02*self.lasty)**3 + (.1*self.flybonus) + .5*(.3*self.digestion)**3)
        else:
            self.energy -= ((.05*self.strength) + (.01*self.lastx)**2 + (.01*self.lasty)**2 + (.01*self.digestion)**3)
        if self.energy <= 0:
            self.die()

    def attack(self, bug):
        if not ((not self.fly) and (hasattr(bug, 'fly') and bug.fly)):
            if not bug.__class__.__name__ == self.__class__.__name__:
                actualstr = 3 + self.strength - self.strdebuff
                enemystr = bug.strength - bug.strdebuff
                if actualstr > enemystr:
                    self.energy += bug.energy
                    self.strdebuff += .3*enemystr
                    helper.killbug(bug)
                elif enemystr < actualstr:
                    bug.energy += self.energy
                    bug.strdebuff += .3*actualstr
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
