import helper
from .bugnaive import Bug
from .ant import WorkerAnt

class QueenAnt(Bug):
    digestion = 10
    energy = 600
    moves = [0.3, 0.3, 0.3, 0.3]
    #          Worker Queen
    birthprob = [2000,1]
    strength = 4
    colour = "yellow"
    classfriendly = True
    jump = False
    Queen = None
    childhood = 100
    birthenergy = 1

    def __init__(self, x, y, birthprobs=None, **kwargs):
        super().__init__(x, y, **kwargs)
        if birthprobs:
            self.birthprobs = birthprobs
        self.immunity = self.childhood

    def step(self):
        if self.immunity > 0:
            self.movemult = 40
        else:
            self.movemult = 1
        super().step()

    def attack(self, bug):
        pass

    def energyloss(self):
        self.energy -= ((.01*self.strength) + (.1*self.lastx)**2 + (.1*self.lasty)**2)
        if self.energy <= 0:
            helper.killbug(self)

    def reproduce(self):
        if self.immunity > 0:
            return
        index = self.randmove(self.birthprob)
        if index == 0:
            newmoves = list()
            for move in range(4):
                newmoves.append(self.mutate(1.5))
            newprobs = list()
            for move in range(4):
                newprobs.append(self.mutate(25))
            newhost = list()
            for host in range(2):
                newhost.append(self.mutate(50))
            newstr = self.mutate(0.6)
            newdig = self.mutate(4)
            helper.makebug(WorkerAnt(self.x, self.y, Queen=self, moves=newmoves, movechance=newprobs, strength=newstr, digestion=newdig, hostility=newhost))
        elif index == 1:
            newmoves = list()
            for move in self.moves:
                newmoves.append(self.mutate(move))
            newprobs = list()
            for move in self.movechance:
                newprobs.append(self.mutate(move))
            newbirths = list()
            newbirths.append(500)
            newbirths.append(self.mutate(self.birthprob[1]))
            newstr = self.mutate(self.strength)
            newdig = self.mutate(self.digestion)
            helper.makebug(self.__class__(self.x, self.y, moves=newmoves, movechance=newprobs, strength=newstr, digestion=newdig))
