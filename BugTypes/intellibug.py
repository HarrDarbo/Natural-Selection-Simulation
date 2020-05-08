import math
import random

import helper
from .bugnaive import Bug

class IntelliBug(Bug):
    colour = "brown"

    hostility = [25,75]
    energy = 40

    target = None
    sight = 10
    chase = 0
    patience = 20
    sightbonus = 1

    def direc(self):
        if not self.target:
            # Attack
            self.chase = 0
            if self.randmove(self.hostility) == 0:
                self.target = helper.findenemy(self.x, self.y, self.sight*self.sightbonus)
                if self.target:
                    # If too slow or too weak
                    if self.mutate(self.target.speed()) > self.speed()*0.75 or self.mutate(self.target.strength) > self.strength:
                        # If classfriendly or if theyre immune or its urself
                        if (self.classfriendly and self.target.__class__.__name__ == self.__class__.__name__) or self.target.immune() or self.target == self:
                            self.target = None
            # If no attack or no enemy in range, eat food
            if not self.target:
                self.target = helper.findfood(self.x, self.y, self.sight*self.sightbonus)
                # nothing at all in sight
                if not self.target:
                    return super().direc()
        # Target aquired
        if self.target:
            if self.target not in helper.foods and self.target not in helper.bugs:
                self.target = None
                return self.direc()
            else:
                self.chase += 1
                if self.chase > self.patience:
                    self.target = None
                    return self.direc()
                return self.chasetarget()
        return super().direc()

    def direcOLD(self):
        if not self.target or not (self.target in helper.bugs or self.target in helper.foods):
            # Find Potential Enemy
            if self.randmove(self.hostility) == 0:
                self.target = helper.findenemy(self.x, self.y, self.sight*self.sightbonus)
                self.chase = 0
                if self.target:
                    if self.mutate(self.target.speed()) > self.speed() or self.strength <= self.mutate(self.target.strength):
                        if (self.classfriendly and self.target.__class__.__name__ == self.__class__.__name__) or self.target.immune() or self.target not in helper.bugs:
                            target = None
            # Otherwise, target food
            if not self.target:
                self.target = helper.findfood(self.x, self.y, self.sight*self.sightbonus)
                self.chase = 0
                if not self.target or self.target not in helper.foods:
                    return super().direc()
        if self.target:
            self.chase += 1
            if self.chase > self.patience:
                self.target = None
            else:
                if issubclass(self.target.__class__, (Bug)):
                    if helper.distbug(self.x, self.y, self.target) - (self.speed()-(self.mutate(self.target.speed()))) >= self.speed()*(self.patience/2):
                        self.target = None
                    else:
                        return self.chasetarget()
                else:
                    return self.chasetarget()
        super().direc()

    def chasetarget(self):
        sign = lambda a: 1 if a>0 else -1
        if abs(self.x - self.target.x) >= abs(self.y - self.target.y):
            if sign(self.x - self.target.x) == 1:
                if self.jump and abs(self.x - self.target.x) < self.moves[3]*self.movemult:
                    self.movemult = self.movemult * (abs(self.x - self.target.x)/self.moves[3])
                return 3
            else:
                if self.jump and abs(self.x - self.target.x) < self.moves[2]*self.movemult:
                    self.movemult = self.movemult * (abs(self.x - self.target.x)/self.moves[2])
                return 2
        else:
            if sign(self.y - self.target.y) == 1:
                if self.jump and abs(self.y - self.target.y) < self.moves[1]*self.movemult:
                    self.movemult = self.movemult * (abs(self.y - self.target.y)/self.moves[1])
                return 1
            else:
                if self.jump and abs(self.y - self.target.y) < self.moves[0]*self.movemult:
                    self.movemult = self.movemult * (abs(self.y - self.target.y)/self.moves[0])
                return 0

    def attack(self, bug):
        if not (self.classfriendly and bug.__class__.__name__ == self.__class__.__name__) and not bug.immune():
            actualstr = 1 + self.strength - self.strdebuff
            enemystr = bug.strength - bug.strdebuff
            if actualstr > enemystr:
                self.energy += .3*bug.energy
                self.strdebuff += enemystr
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
            self.strdebuff -= .1*self.strength
            if self.strdebuff < 0:
                self.strdebuff = 0
