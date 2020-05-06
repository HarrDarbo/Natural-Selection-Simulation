import random
import helper
import copy
import math

class Bug(object):
    x = None
    y = None
    # Flags (for child classes)
    colour = "brown"
    classfriendly = False
    jump = True
    followfood = True
    # for display and energy
    lastx = 0
    lasty = 0
    prevx = 0
    prevy = 0
    ate = False
    # genetic deciders
    strength = 3
    strdebuff = 0
    energy = 40
    birthenergy = 30
    #        N S E W
    moves = [1,1,1,1]
    #             N  S  E  W
    movechance = [25,25,25,25]
    movemult = 1
    #            Y  N
    hostility = [50,50]
    # childhood immunity, also stops first turn step
    childhood = 25
    immunity = childhood
    # energy gain from food
    digestion = 10
    def __init__(self, x, y, moves=None, movechance=None, strength=None, digestion=None, hostility=None):
        self.x = x
        self.y = y
        if moves:
            self.moves = moves
        if movechance:
            self.movechance = movechance
        if strength:
            self.strength = strength
        if digestion:
            self.digestion = digestion
        if hostility:
            self.hostility = hostility

    def step(self):
        self.immunity -= 1
        if self.immunity == self.childhood-1:
            return
        self.prevx = self.x
        self.prevy = self.y

        index = self.randmove(self.movechance)
        if self.ate:
            # Continue moving in the same direction if you ate
            self.ate = False
            self.y += self.lasty
            self.x += self.lastx
        else:
            # random movement options
            if index == 0:
                self.y+=self.moves[0]*self.movemult
                self.lasty = self.moves[0]*self.movemult
                self.lastx = 0
            elif index == 1:
                self.y-=self.moves[1]*self.movemult
                self.lasty = -1*self.moves[1]*self.movemult
                self.lastx = 0
            elif index == 2:
                self.x+=self.moves[2]*self.movemult
                self.lastx = self.moves[2]*self.movemult
                self.lasty = 0
            elif index == 3:
                self.x-=self.moves[3]*self.movemult
                self.lastx = -1*self.moves[3]*self.movemult
                self.lasty = 0
        # border control
        if self.x < 0:
            self.lastx -= self.x
            self.x = 0
        elif self.x > helper.clen:
            self.lastx -= (self.x-helper.clen)
            self.x = helper.clen
        if self.y < 0:
            self.lasty -= self.y
            self.y = 0
        elif self.y > helper.clen:
            self.lasty -= (self.y-helper.clen)
            self.y = helper.clen

        helper.movebug(self)
        self.eat()
        helper.attackbug(self)
        self.energyloss()

    def eat(self):
        foodgain = 0
        if not self.jump:
            sign = lambda a: 1 if a>0 else -1
            if self.lastx != 0:
                for n in range(int(abs(self.lastx)+0.5)):
                    foodgain += helper.eatfood(int(self.x+.5)-((n*sign(self.lastx))+1), int(self.y+.5)-1) * self.digestion
            if self.lasty != 0:
                for n in range(int(abs(self.lasty)+0.5)):
                    foodgain += helper.eatfood(int(self.x+.5)-1, int(self.y+.5)-((n*sign(self.lasty))+1)) * self.digestion
        else:
            foodgain = helper.eatfood(int(self.x+.5)-1, int(self.y+.5)-1) * self.digestion
        self.energy += foodgain
        if self.followfood and foodgain > 0:
            self.ate = True
        if self.energy > 50 + math.log(self.digestion):
            self.energy -= self.birthenergy
            self.reproduce()

    def energyloss(self):
        self.energy -= ((.1*self.strength) + (.1*self.lastx)**2 + (.1*self.lasty)**2 + 0.4*(.04*self.digestion)**4)
        if self.energy <= 0:
            helper.killbug(self)

    def die(self):
        del self

    def reproduce(self):
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
        helper.makebug(self.__class__(self.x, self.y, moves=newmoves, movechance=newprobs, strength=newstr, digestion=newdig, hostility=newhost))

    def attack(self, bug):
        if self.randmove(self.hostility) == 0 and not (self.classfriendly and bug.__class__.__name__ == self.__class__.__name__) and not bug.immune():
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

    def immune(self):
        return self.immunity > 0

    def randmove(self, list):
        chance = 0
        for item in list:
            chance += item
        num = random.random()*chance
        index = 0
        for n in list:
            num -= n
            if num <= 0:
                return index
            index += 1
        return 0

    def mutate(self, gene):
        return gene+(gene*((random.random()*.2)-(.1)))
