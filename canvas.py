import time

from tkinter import *

import helper
from BugTypes import *

class HCanvas(object):
    canvas = None
    tkbugs = dict()
    tkfoods = dict()
    root = None
    scale = 2
    def __init__(self):
        self.root = Tk()
        self.root.title("Stee's Bug Sim")
        self.root.geometry('810x805')
        self.canvas = Canvas(self.root, height=self.scale*(helper.clen+2), width=self.scale*(helper.clen+2), bg='black')
        self.canvas.pack()

    def step(self):
        # Bugs
        for bug in helper.bugs:
            if bug in self.tkbugs.keys():
                foundbug = self.tkbugs[bug]
                self.canvas.move(
                    foundbug, self.scale*bug.lastx, self.scale*bug.lasty)
            else:
                colour = bug.colour
                self.tkbugs[bug] = self.canvas.create_rectangle(self.scale*bug.x, self.scale*bug.y, self.scale*(bug.x+1), self.scale*(bug.y+1), fill=colour, outline=colour)
        for bug in list(set(self.tkbugs.keys()) - set(helper.bugs)):
            self.canvas.delete(self.tkbugs[bug])
            self.tkbugs.pop(bug)

        # Food
        for food in helper.foods:
            if food not in self.tkfoods.keys():
                self.tkfoods[food] = self.canvas.create_rectangle(self.scale*food.x, self.scale*food.y, self.scale*(food.x+1), self.scale*(food.y+1), fill="green", outline="green")
        for food in list(set(self.tkfoods.keys()) - set(helper.foods)):
            self.canvas.delete(self.tkfoods[food])
            self.tkfoods.pop(food)


        self.root.update()
