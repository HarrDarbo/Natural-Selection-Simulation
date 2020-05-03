import random
import helper

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
    def __init__(self, x, y, moves=[1,1,1,1], movechance=[25,25,25,25], strength=5):
        self.x = x
        self.y = y
        self.moves = moves
        self.movechance = movechance
        self.strength = strength

    def step(self):
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
        self.energyloss()

    def eat(self):
        self.energy += helper.eatfood(int(self.x+.5)-1, int(self.y+.5)-1) * 10
        if self.energy > 50:
            self.energy -= 30
            self.reproduce()

    def energyloss(self):
        self.energy -= ((.02*self.strength) + (.02*self.moves[0]) + (.02*self.moves[1]) + (.02*self.moves[2]) + (.02*self.moves[3]))
        if self.energy <= 0:
            helper.bugs.remove(self)
            del self

    def reproduce(self):
        helper.bugs.append(Bug(self.x, self.y, self.moves, self.movechance, self.strength))

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
