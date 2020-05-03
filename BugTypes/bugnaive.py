import random
import helper
import copy

class Bug(object):
    x = None
    y = None
    #        N S E W
    moves = [1,1,1,1]
    #             N  S  E  W
    movechance = [25,25,25,25]
    # for display and energy
    lastx = 0
    lasty = 0
    # genetic deciders
    strength = 5
    energy = 50
    # childhood immunity
    immunity = 50
    # energy gain from food
    digestion = 10
    def __init__(self, x, y, moves=[1,1,1,1], movechance=[25,25,25,25], strength=5, digestion = 10):
        self.x = x
        self.y = y
        self.moves = moves
        self.movechance = movechance
        self.strength = strength

    def step(self):
        self.immunity -= 1
        index = self.randmove()
        # random movement options
        if index == 0:
            self.y+=self.moves[0]
            self.lasty = self.moves[0]
            self.lastx = 0
        elif index == 1:
            self.y-=self.moves[1]
            self.lasty = -1*self.moves[1]
            self.lastx = 0
        elif index == 2:
            self.x+=self.moves[2]
            self.lastx = self.moves[2]
            self.lasty = 0
        elif index == 3:
            self.x-=self.moves[3]
            self.lastx = -1*self.moves[3]
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
        self.eat()
        self.attack()
        self.energyloss(index)

    def eat(self):
        self.energy += helper.eatfood(int(self.x+.5)-1, int(self.y+.5)-1) * self.digestion
        if self.energy > 50:
            self.energy -= 30
            self.reproduce()

    def energyloss(self, index):
        self.energy -= ((.02*self.strength) + (.1*self.lastx) + (.1*self.lasty))
        if self.energy <= 0:
            self.die()

    def die(self):
        try:
            helper.bugs.remove(self)
        except ValueError:
            pass
        del self

    def reproduce(self):
        newmoves = list()
        for move in self.moves:
            newmoves.append(move+(random.random()*.2*move)-(.1*move))
        newprobs = list()
        for move in self.movechance:
            newprobs.append(move+(random.random()*.2*move)-(.1*move))
        newstr = self.strength+(random.random()*.2*self.strength)-(.1*self.strength)
        helper.bugs.append(self.__class__(self.x, self.y, newmoves, newprobs, newstr))

    def attack(self):
        for bug in helper.bugs:
            if int(bug.x) == int(self.x) and int(bug.y) == int(self.y) and bug.immunity <= 0:
                if self.strength > bug.strength:
                    self.energy += .5*bug.energy
                    bug.die()
                elif bug.strength < self.strength:
                    bug.energy += .5*self.energy
                    self.die()
                elif self.energy > bug.energy:
                    self.energy -= 0.5*bug.energy
                    bug.die()
                elif bug.energy > self.energy:
                    bug.energy -= 0.5*self.energy
                    self.die()


    def randmove(self):
        chance = self.movechance[0]+self.movechance[1]+self.movechance[2]+self.movechance[3]
        num = random.random()*chance
        index = 0
        for n in self.movechance:
            num -= n
            if num <= 0:
                return index
            index += 1
        return 3
