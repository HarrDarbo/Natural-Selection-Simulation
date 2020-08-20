import string
import os
import math
import random
import threading

from food import *
from BugTypes import *

def init():
    # other
    global canvas
    canvas = None
    global clen
    clen = 150
    global stats
    stats = 'No generated statistics yet'
    global BugSpawns
    BugSpawns = [GrowBug, GenericFly]
    global SpecialSpawns
    SpecialSpawns = [GenericQueenAnt, GenericQueenBee]
    global ExtraSpawns
    ExtraSpawns = [GenericWorkerAnt, GenericWorkerBee]
    global AllSpawns
    AllSpawns = []
    for i in BugSpawns + SpecialSpawns + ExtraSpawns:
        AllSpawns.append(i)
    global OldSpawns
    OldSpawns = [Beetle, Fly, DragonFly, QueenAnt, LowFly, Tick]

    # Run parameters
    global foodspawn
    foodspawn = 8
    global bugspawn
    bugspawn = 0
    global bugspawntimer
    bugspawntimer = 100
    global Freeze
    Freeze = False

    # Bug tracking
    global bugs
    bugs = list()
    global buggrid
    buggrid = []
    for n in range(clen):
        buggrid.append([])
        for m in range(clen):
            buggrid[n].append([])

    # Food Tracking
    global foods
    foods = list()
    global plantenable
    plantenable = True
    global foodgrid
    foodgrid = []
    for n in range(clen):
        foodgrid.append([])
        for m in range(clen):
            foodgrid[n].append([])

def makebug(bug):
    bugs.append(bug)
    buggrid[int(bug.x+.5)-1][int(bug.y+.5)-1].append(bug)

def spawnbugs(amt):
    for bug in BugSpawns:
        for n in range(amt):
            makebug(bug(int(random.random()*clen)-1, int(random.random()*clen)-1))
    for bug in SpecialSpawns:
        for n in range(int(amt/5)):
            makebug(bug(int(random.random()*clen)-1, int(random.random()*clen)-1))

def spawnbug(name, amt):
    for bug in AllSpawns:
        if name == bug.__name__:
            for n in range(amt):
                makebug(bug(int(random.random()*clen)-1, int(random.random()*clen)-1))

def spawnbug(name, amt, x, y):
    x = int(x+.5)-1
    y = int(y+.5)-1
    for bug in AllSpawns:
        if name == bug.__name__:
            for n in range(amt):
                makebug(bug(x, y))

def movebug(bug):
    try:
        buggrid[int((bug.x-bug.lastx)+.5)-1][int((bug.y-bug.lasty)+.5)-1].remove(bug)
        buggrid[int(bug.x+.5)-1][int(bug.y+.5)-1].append(bug)
    except ValueError:
        # Threading synchronicity cuases problems; death before movement
        pass

def findenemy(xp, yp, dist):
    x = int(xp+0.5)-1
    y = int(yp+0.5)-1
    misplace = int(random.random()*4)*.5*math.pi
    for d in range(int(dist+.5)):
        for i in range(4*d):
            ang = (math.radians(i*(360/(4*d))) + misplace) % 2*math.pi
            try:
                if len(buggrid[int(x+d*math.sin(ang)+0.5)-1][int(y+d*math.cos(ang)+0.5)-1]) > 0 and random.random() <= buggrid[int(x+d*math.sin(ang)+0.5)-1][int(y+d*math.cos(ang)+0.5)-1][0].standout:
                    return buggrid[int(x+d*math.sin(ang)+0.5)-1][int(y+d*math.cos(ang)+0.5)-1][0]
            except IndexError:
                pass
    return None


def distance(xs, ys, obj):
    return math.sqrt((xs-obj.x)**2 + (ys-obj.y)**2)

def attackbug(bug):
    for enemy in buggrid[int(bug.x+.5)-1][int(bug.y+.5)-1]:
        if enemy != bug:
            bug.attack(enemy)

def killbug(bug):
    try:
        bugs.remove(bug)
    except ValueError:
        pass
    try:
        buggrid[int(bug.x+.5)-1][int(bug.y+.5)-1].remove(bug)
    except ValueError:
        pass
    bug.die()

def makerandomfood():
    food = Food()
    foods.append(food)
    foodgrid[int(food.x+.5)-1][int(food.y+.5)-1].append(food)

def makerandombush():
    bush = Bush()
    foods.append(bush)
    foodgrid[int(bush.x+.5)-1][int(bush.y+.5)-1].append(bush)

def makefood(x,y):
    try:
        food = Food(x,y)
        foods.append(food)
        foodgrid[int(food.x+.5)-1][int(food.y+.5)-1].append(food)
    except IndexError:
        # Trees do this
        pass

def makebush(x,y):
    food = Bush(x,y)
    foods.append(food)
    foodgrid[int(food.x+.5)-1][int(food.y+.5)-1].append(food)

def findfood(xp, yp, dist):
    x = int(xp+0.5)-1
    y = int(yp+0.5)-1
    misplace = int(random.random()*2)*math.pi
    for d in range(int(dist+.5)):
        for i in range(4*d):
            ang = (math.radians(i*(90/d)) + (misplace % (90/d)))
            try:
                ct = len(foodgrid[int(x+d*math.cos(ang)+0.5)-1][int(y+d*math.sin(ang)+0.5)-1])
                for e in range(ct):
                    if isinstance(foodgrid[int(x+d*math.sin(ang)+0.5)-1][int(y+d*math.cos(ang)+0.5)-1][e], Food):
                        return foodgrid[int(x+d*math.sin(ang)+0.5)-1][int(y+d*math.cos(ang)+0.5)-1][e]
            except IndexError:
                pass
    return None

def findbushes(xp, yp, dist):
    x = int(xp+0.5)-1
    y = int(yp+0.5)-1
    bushcount = 0
    for d in range(int(dist+.5)):
        for i in range(4*d):
            ang = math.radians(i*(360/(4*d)))
            try:
                ct = len(foodgrid[int(x+d*math.sin(ang)+0.5)-1][int(y+d*math.cos(ang)+0.5)-1])
                for e in range(ct):
                    if isinstance(foodgrid[int(x+d*math.sin(ang)+0.5)-1][int(y+d*math.cos(ang)+0.5)-1][e], Bush):
                        bushcount += 1
            except IndexError:
                pass
    return max(bushcount, 1)

def eatfood(xp, yp):
    x = int(xp+0.5)-1
    y = int(yp+0.5)-1
    amt = len(foodgrid[x][y])
    if amt > 0:
        amt = 0
        for food in foodgrid[x][y]:
            if issubclass(food.__class__, Food):
                foods.remove(food)
                foodgrid[x][y].remove(food)
                food.die()
                del food
                amt += 1
    return amt

def delfood(xp,yp):
    x = int(xp+0.5)-1
    y = int(yp+0.5)-1
    for food in foodgrid[x][y]:
        foods.remove(food)
        foodgrid[x][y].remove(food)
        food.die()
        del food

def foodrate(rate):
    global foodspawn
    foodspawn = rate

def bugrate(rate):
    global bugspawn
    bugspawn = rate

def bugratetimer(rate):
    global bugspawntimer
    bugspawntimer = rate

def flipplants():
    global plantenable
    plantenable = not plantenable

def reset():
    bugs.clear()
    buggrid.clear()
    for n in range(clen):
        buggrid.append([])
        for m in range(clen):
            buggrid[n].append([])
    foods.clear()
    foodgrid.clear()
    for n in range(clen):
        foodgrid.append([])
        for m in range(clen):
            foodgrid[n].append([])
    global foodspawn
    foodspawn = 0
    global bugspawn
    bugspawn = 0
    global bugspawntimer
    bugspawntimer = 100

def freeze():
    global Freeze
    Freeze = not Freeze

def allstep():
    multithread = True
    if multithread:
        threadnum = int(len(bugs)/25)+1
        if threadnum > 500:
            threadnum = 500
        threads = list()
        for x in range(threadnum):
            threads.append(threading.Thread(target=allstepthread, daemon=True, args=(x,threadnum,)))
            threads[x].start()
        for thread in threads:
            thread.join()
    else:
        for bug in bugs:
            bug.step()
    for food in foods:
        if issubclass(food.__class__, Bush):
            food.step()

def allstepthread(indx,threadnum):
    start = int((len(bugs)*indx)/threadnum)
    end = int((len(bugs)*(indx+1))/threadnum)
    for bug in bugs[start:end]:
        bug.step()

def statistics():
    if len(bugs) <= 0:
        return 'No active bugs'
    avgstr = 0
    avgspd = 0
    avgstout = 0
    avghostile = [0,0]
    avgsight = 0
    avgpat = 0
    friendly = 0
    jumps = 0
    flys = 0
    queens = 0
    wrks = 0
    psns = 0
    for bug in bugs:
        if bug.classfriendly:
            friendly += 1
        if bug.jump:
            jumps += 1
        if bug.fly:
            flys += 1
        if bug.queen:
            queens += 1
        if bug.worker:
            wrks += 1
        if bug.poisonous:
            psns += 1
        avgstr += bug.strength
        avgspd += bug.speed
        avgstout += bug.standout
        avghostile[0] += bug.hostility[0]
        avghostile[1] += bug.hostility[1]
        avgsight += bug.sight
        avgpat += bug.patience
    bugcount = len(bugs)
    avgstr = avgstr/bugcount
    avgspd = avgspd/bugcount
    avgstout = avgstout/bugcount
    avghostile[0] = avghostile[0]/bugcount
    avghostile[1] = avghostile[1]/bugcount
    avgsight = avgsight/bugcount
    avgpat = avgpat/bugcount

    stats = 'Bug Count: ' + str(bugcount)
    stats += '\nAvg Strength: ' + str(avgstr)[:5] + '\nAvg Speed: ' + str(avgspd)[:5] + '\nAvg Standout: ' + str(avgstout)[:5] + '\nAvg Hostility: ' + str(avghostile[0]/(2*avghostile[1]))[:5] + '\nAvg Sight: ' + str(avgsight)[:5] + '\nAvg Patience: ' + str(avgpat)[:5]
    stats += '\nFriendly: ' + str(friendly) + ' (' + str((friendly/bugcount)*100)[:4] + '%)'
    stats += '\nJumping: ' + str(jumps) + ' (' + str((jumps/bugcount)*100)[:4] + '%)'
    stats += '\nFlying: ' + str(flys) + ' (' + str((flys/bugcount)*100)[:4] + '%)'
    stats += '\nQueens: ' + str(queens) + ' (' + str((queens/bugcount)*100)[:4] + '%)'
    stats += '\nWorkers: ' + str(wrks) + ' (' + str((wrks/bugcount)*100)[:4] + '%)'
    stats += '\nEusocial: ' + str(wrks+queens) + ' (' + str(((queens+wrks)/bugcount)*100)[:4] + '%)'
    stats += '\nPoisonous: ' + str(psns) + ' (' + str((psns/bugcount)*100)[:4] + '%)'

    return stats
