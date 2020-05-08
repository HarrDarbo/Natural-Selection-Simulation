import random

import helper
from .intellibug import IntelliBug

class Fly(IntelliBug):
    colour = "white"
    strength = 1
    digestion = 10
    fly = False
    birthenergy = 30
    flybonus = 2
    sight = 5
    patience = 25
    #         Land Fly
    landchance=[50,50]

    def __init__(self, x, y, landchance=None, flybonus=None, **kwargs):
        super().__init__(x, y, **kwargs)
        if landchance:
            self.landchance = landchance
        if flybonus:
            self.flybonus = flybonus

    def step(self):
        index = self.randmove(self.landchance)
        if index == 0:
            self.fly = False
            self.movemult = 1
            self.sightbonus = 1
        elif index == 1:
            self.fly = True
            self.movemult = self.flybonus
            self.sightbonus = 3
        super().step()

    def eat(self):
        if not self.fly:
            super().eat()

    def energyloss(self):
        if self.fly:
            self.energy -= ((.4*self.strength) + (.2*self.lastx)**2 + (.2*self.lasty)**2 + (.1*self.flybonus) + .3*(.1*self.digestion)**3)
        else:
            self.energy -= ((.3*self.strength) + (.05*self.lastx)**2 + (.05*self.lasty)**2 + 0.3*(.04*self.digestion)**3)
        if self.energy <= 0:
            self.die()

    def attack(self, bug):
        if not self.fly:
            super().attack(bug)
        if self.fly and hasattr(bug, 'fly') and bug.fly:
            super().attack(bug)

    def reproduce(self):
        newflys = list()
        for fly in self.landchance:
            newflys.append(self.mutate(fly))
        newmoves = list()
        for move in self.moves:
            newmoves.append(self.mutate(move))
        newprobs = list()
        for move in self.movechance:
            newprobs.append(self.mutate(move))
        newhost = list()
        for host in self.hostility:
            newhost.append(self.mutate(host))
        newstr = self.mutate(self.strength)
        newdig = self.mutate(self.digestion)
        newbonus = self.mutate(self.flybonus)
        helper.makebug(self.__class__(self.x, self.y, landchance=newflys, flybonus=newbonus, moves=newmoves, movechance=newprobs, strength=newstr, digestion=newdig, hostility=newhost))
