import random

import helper
from .intellibug import IntelliBug

class Tick(IntelliBug):
    digestion = 5
    strength = 4
    hostility = [100,1]

    colour = "red"
    jump = False
    followfood = False
    classfriendly = True

    sight = 12
    patience = 35

    def immune(self):
        return random.random() > 0.5

    def energyloss(self):
        self.energy -= ((.2*self.strength) + (.1*self.lastx)**2 + (.1*self.lasty)**2 + .1*(.2*self.digestion)**3)
        if self.energy <= 0:
            helper.killbug(self)

    def attack(self, bug):
        if not (self.classfriendly and bug.__class__.__name__ == self.__class__.__name__) and not bug.immune():
            actualstr = 2 + self.strength - self.strdebuff
            enemystr = bug.strength - bug.strdebuff
            if actualstr > enemystr:
                self.energy += bug.energy
                self.strdebuff += 0.7*enemystr
                helper.killbug(bug)
            elif enemystr < actualstr:
                bug.energy += .3*self.energy
                bug.strdebuff += actualstr
                helper.killbug(self)
            elif self.energy > bug.energy:
                self.energy -= 0.5*bug.energy
                helper.killbug(bug)
            elif bug.energy > self.energy:
                bug.energy -= 0.5*self.energy
                helper.killbug(self)
        if self.strdebuff > 0:
            self.strdebuff -= 0.25*self.strength
            if self.strdebuff < 0:
                self.strdebuff = 0
