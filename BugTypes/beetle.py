import helper
from .intellibug import IntelliBug

class Beetle(IntelliBug):
    digestion = 7
    colour = "magenta"
    classfriendly = True
    jump = False
    followfood = True

    def energyloss(self):
        self.energy -= ((.1*self.strength) + (.1*self.lastx)**2 + (.1*self.lasty)**2 + (.1*self.digestion)**3)
        if self.energy <= 0:
            helper.killbug(self)
