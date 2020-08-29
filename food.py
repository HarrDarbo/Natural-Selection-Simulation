import helper
import random

class Food(object):
    x = 0
    y = 0
    colour = 'green'
    parent = None
    def __init__(self,x=None,y=None,parent=None):
        if x:
            self.x = x
        else:
            self.x = int(random.random()*helper.clen)
        if y:
            self.y = y
        else:
            self.y = int(random.random()*helper.clen)
        self.parent = parent

    def die(self):
        if random.random() > 0.9995 and helper.plantenable:
            helper.makebush(self.x, self.y)
        if self.parent:
            self.parent.size += 0.02

class Bush(object):
    x = 0
    y = 0
    colour = '#CFFF80'
    size = 0
    seed = 0
    def __init__(self,x=None,y=None):
        if x:
            self.x = max(0, min(x, helper.clen-1))
        else:
            self.x = int(random.random()*helper.clen)
        if y:
            self.y = max(0, min(y, helper.clen-1))
        else:
            self.y = int(random.random()*helper.clen-1)
        self.size = 1
        self.seed = int(random.random()*15)+10
        self.seed = self.seed / helper.findbushes(self.x, self.y, self.seed)

    def step(self):
        self.size += 0.02
        agediff = 30-((0.4*self.size-5)*(0.4*self.size-5))
        agediff = 100-max(50, agediff + 50)
        for x in range(max(int(self.size/agediff),1)):
            newx = (self.x-(self.size*.5)) + (random.random()*self.size)
            newy = (self.y-(self.size*.5)) + (random.random()*self.size)
            newx = max(0, min(newx, helper.clen-1))
            newy = max(0, min(newy, helper.clen-1))
            self.seed -= 0.01*(len(helper.foodgrid[int(newx+0.5)-1][int(newy+0.5)-1]))
            helper.makefood(newx,newy)
        if self.size > self.seed*3:
            helper.delfood(self.x, self.y)

    def die(self):
        for x in range(10*int(self.size)):
            helper.makefood((self.x-(self.size*.5)) + (random.random()*self.size), (self.y-(self.size*.5)) + (random.random()*self.size))
