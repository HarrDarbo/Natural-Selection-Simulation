import time
import random

from tkinter import *

import helper
from BugTypes import *

class HCanvas(object):
    canvas = None
    frame = None
    tkbugs = dict()
    tkfoods = dict()
    root = None
    scale = 5
    gui = dict()
    currentbug = Bug

    def __init__(self):
        self.root = Tk()
        self.root.title("Stee's Bug Sim")
        geo = str(int(self.scale*helper.clen+265)) + 'x' + str(int(self.scale*helper.clen+5))
        self.root.geometry(geo)
        self.root.configure(bg='black')
        self.canvas = Canvas(self.root, height=self.scale*(helper.clen+2), width=self.scale*(helper.clen+2), bg='black')
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.grid(row=0,column=0,rowspan=200)
        self.sidemenu()

    def sidemenu(self):
        # CLEAR: Top Left Of Screen
        self.gui['clear'] = Button(self.root, text="CLEAR BOARD", command=self.reset, width=15)
        self.gui['clear'].grid(row=0, column=1)
        # EXIT: Right of Clear, Top
        self.gui['exit'] = Button(self.root, text="EXIT", command=self.quit, width=15)
        self.gui['exit'].grid(row=0,column=2)
        # FLAT FOOD SPAWN TEXT BOX: Below Top Options
        self.gui['flatfoodbox'] = Entry(self.root, width=15)
        self.gui['flatfoodbox'].insert(INSERT, '100')
        self.gui['flatfoodbox'].grid(row=1,column=2)
        # FLAT FOOD SPAWN BUTTON: Right of text box
        self.gui['flatfoodbutton'] = Button(self.root, text="Spawn Food", command=self.spawnfood, width=15)
        self.gui['flatfoodbutton'].grid(row=1,column=1)
        # FOOD SPAWN RATE TEXT BOX: Below flat spawn
        self.gui['foodbox'] = Entry(self.root, width=15)
        self.gui['foodbox'].insert(INSERT, str(helper.foodspawn))
        self.gui['foodbox'].grid(row=2,column=2)
        # FOOD SPAWN RATE BUTTON: Right of text box
        self.gui['foodbutton'] = Button(self.root, text="Set Food Rate", command=self.changefood, width=15)
        self.gui['foodbutton'].grid(row=2,column=1)
        # FLAT BUG SPAWN TEXT BOX
        self.gui['bugallbox'] = Entry(self.root, width=15)
        self.gui['bugallbox'].insert(INSERT, '5')
        self.gui['bugallbox'].grid(row=3,column=2)
        # FLAT BUG SPAWN BUTTON: Right of text box
        self.gui['bugallbutton'] = Button(self.root, text="Spawn All Bugs", command=self.spawnbugs, width=15)
        self.gui['bugallbutton'].grid(row=3,column=1)
        # BUG SPAWN RATE TEXT BOX: Below flat spawn
        self.gui['bugratebox'] = Entry(self.root, width=15)
        self.gui['bugratebox'].insert(INSERT, str(helper.bugspawn))
        self.gui['bugratebox'].grid(row=4,column=2)
        # BUG SPAWN RATE BUTTON: Right of text box
        self.gui['bugratebutton'] = Button(self.root, text="Set Bug Rate", command=self.changebugs, width=15)
        self.gui['bugratebutton'].grid(row=4,column=1)
        # BUG SPAWN RATE TIME TEXT BOX: Below bug spawn rate
        self.gui['bugratetimebox'] = Entry(self.root, width=15)
        self.gui['bugratetimebox'].insert(INSERT, '100')
        self.gui['bugratetimebox'].grid(row=5,column=2)
        # BUG SPAWN RATE TIME BUTTON: Right of text box
        self.gui['bugratetimebutton'] = Button(self.root, text="Bug Spawn Time", command=self.changebugtime, width=15)
        self.gui['bugratetimebutton'].grid(row=5,column=1)
        # SPAWN SPECIFIC BUG: Below Bug Spawn Rate Time
        self.currentbug = StringVar()
        self.currentbug.set('GrowBug')
        self.gui['buglist'] = OptionMenu(self.root, self.currentbug, *(i.__name__ for i in helper.OldSpawns))
        self.gui['buglist'].grid(row=6,column=2)
        # SPCIFIC BUG SPAWN BUTTON
        self.gui['buglistbutton'] = Button(self.root, text="Specific Bug Spawn", command=self.spawnbugs, width=15)
        self.gui['buglistbutton'].grid(row=6,column=1)
        # SPECIFIC BUG SPAWN COUNT
        self.gui['buglistamtbox'] = Entry(self.root, width=15)
        self.gui['buglistamtbox'].insert(INSERT, '1')
        self.gui['buglistamtbox'].grid(row=7,column=2)
        # ENABLE/DISABLE PLANTS
        self.gui['plantspawnbutton'] = Button(self.root, text="Enable/Disable Plants", command=self.enableplants, width=15)
        self.gui['plantspawnbutton'].grid(row=7,column=1)

        # GENERATE STATISTICS BUTTON
        self.gui['statisticsbutton'] = Button(self.root, text="Generate Statistics", command=self.statize, width=15)
        self.gui['statisticsbutton'].grid(row=19,column=1)
        # STATS BOX
        self.gui['statisticsmessage'] = Message(self.root, text="No stats", width=150, padx=2, pady=1)
        self.gui['statisticsmessage'].grid(row=19,column=2)

        # FREEZE SIM: Bottom of commands
        self.gui['bugratetimebutton'] = Button(self.root, text="FREEZE SIM", command=helper.freeze, width=15)
        self.gui['bugratetimebutton'].grid(row=20,column=1)

    def changefood(self):
        rate = self.gui['foodbox'].get()
        helper.foodrate(int(rate))

    def changebugs(self):
        rate = self.gui['bugratebox'].get()
        helper.bugrate(int(rate))

    def changebugtime(self):
        rate = self.gui['bugratetimebox'].get()
        helper.bugratetimer(int(rate))

    def spawnfood(self):
        amt = self.gui['flatfoodbox'].get()
        for n in range(int(amt)):
            helper.makerandomfood()

    def spawnbugs(self):
        amt = self.gui['bugallbox'].get()
        helper.spawnbugs(int(amt))

    def spawnbug(self):
        amt = self.gui['buglistamtbox'].get()
        helper.spawnbug(self.currentbug.get(), int(amt))

    def enableplants(self):
        helper.flipplants()

    def statize(self):
        self.gui['statisticsmessage'].configure(text=helper.statistics())
        self.root.after(250, self.statize)

    def reset(self):
        helper.reset()
        self.canvas.delete("all")
        self.tkbugs = {}
        self.tkfoods = {}
        self.gui['foodbox'].delete(0, 'end')
        self.gui['bugratebox'].delete(0, 'end')
        self.gui['bugratetimebox'].delete(0, 'end')
        self.gui['bugratetimebox'].insert(INSERT, '100')

    def quit(self):
        # Yes i do know i am just crashing it but i do not care
        self.root.destroy()

    def click(self, event):
        helper.spawnbug(self.currentbug.get(), 1, event.x/self.scale, event.y/self.scale)

    def step(self):
        # Bugs
        if not helper.Freeze:
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
                    colour = food.colour
                    if colour == '#CFFF80':
                        self.tkfoods[food] = self.canvas.create_oval(self.scale*food.x-(0.5*food.size), self.scale*food.y-(0.5*food.size), self.scale*(food.x+1)+(0.5*food.size), self.scale*(food.y+1)+(0.5*food.size), fill=colour, outline=colour)
                    else:
                        self.tkfoods[food] = self.canvas.create_rectangle(self.scale*food.x, self.scale*food.y, self.scale*(food.x+1), self.scale*(food.y+1), fill=colour, outline=colour)
                elif food.colour == '#CFFF80':
                    self.canvas.delete(self.tkfoods[food])
                    self.tkfoods.pop(food)
                    self.tkfoods[food] = self.canvas.create_oval(self.scale*food.x-(0.5*food.size), self.scale*food.y-(0.5*food.size), self.scale*(food.x+1)+(0.5*food.size), self.scale*(food.y+1)+(0.5*food.size), fill=food.colour, outline='orange')
                    self.canvas.tag_lower(self.tkfoods[food])
            for food in list(set(self.tkfoods.keys()) - set(helper.foods)):
                self.canvas.delete(self.tkfoods[food])
                self.tkfoods.pop(food)
        else:
            for bug in helper.bugs:
                if bug not in self.tkbugs.keys():
                    colour = bug.colour
                    self.tkbugs[bug] = self.canvas.create_rectangle(self.scale*bug.x, self.scale*bug.y, self.scale*(bug.x+1), self.scale*(bug.y+1), fill=colour, outline=colour)

        self.root.update()
