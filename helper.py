import string
import os

from food import Food

def init():
    # other
    global canvas
    canvas = None
    global clen
    clen = 400

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
    global foodgrid
    foodgrid = []
    for n in range(clen):
        foodgrid.append([])
        for m in range(clen):
            foodgrid[n].append([])

def makebug(bug):
    bugs.append(bug)
    buggrid[int(bug.x+.5)-1][int(bug.y+.5)-1].append(bug)

def movebug(bug):
    buggrid[int(bug.prevx+.5)-1][int(bug.prevy+.5)-1].remove(bug)
    buggrid[int(bug.x+.5)-1][int(bug.y+.5)-1].append(bug)

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

def makefood():
    food = Food()
    foods.append(food)
    foodgrid[int(food.x+.5)-1][int(food.y+.5)-1].append(food)

# Doesnt int() coords since the bug is expected to for different eating strategies
def eatfood(x, y):
    amt = len(foodgrid[x][y])
    if amt > 0:
        for food in foodgrid[x][y]:
            foods.remove(food)
            foodgrid[x][y].remove(food)
    return amt

def statistics(types):
    os.system('clear')
    for type in types:
        totalstr = 0
        totalm = [0,0,0,0]
        totalp = [0,0,0,0]
        totalfly = [0,0]
        totalhost = [0,0]
        totalair = 0
        totaldig = 0
        totalbonus = 0
        total = 0
        for bug in bugs:
            if bug.__class__.__name__ == type:
                total+=1
                totalstr+=bug.strength
                totaldig+=bug.digestion
                totalhost[0]+=bug.hostility[0]
                totalhost[1]+=bug.hostility[1]
                for n in range(4):
                    totalm[n] += bug.moves[n]
                    totalp[n] += bug.movechance[n]
                if hasattr(bug, 'fly'):
                    totalair += 1
                    totalfly[0] += bug.landchance[0]
                    totalfly[1] += bug.landchance[1]
                    totalbonus += bug.flybonus
        if total > 0:
            totalhost[0] = totalhost[0]/total
            totalhost[1] = totalhost[1]/total
            overallhost = totalhost[0] + totalhost[1]
            totalstr = totalstr / total
            totaldig = totaldig / total
            if totalair > 0:
                totalfly[0] = totalfly[0] / totalair
                totalfly[1] = totalfly[1] / totalair
                totalbonus = totalbonus / totalair
            overallfly = totalfly[0] + totalfly[1]
            for n in range(4):
                totalm[n] = totalm[n] / total
                totalp[n] = totalp[n] / total
            overallp = totalp[0] + totalp[1] + totalp[2] + totalp[3]
            print("===" + str(type) + "=====================")
            print("|        NORTH SOUTH EAST  WEST  |")
            print("| PROB: ", str(totalp[0]/overallp)[:5].ljust(5), str(totalp[1]/overallp)[:5].ljust(5), str(totalp[2]/overallp)[:5].ljust(5), str(totalp[3]/overallp)[:5].ljust(5), "|")
            print("| DIST: ", str(totalm[0])[:5].ljust(5), str(totalm[1])[:5].ljust(5), str(totalm[2])[:5].ljust(5), str(totalm[3])[:5].ljust(5)    , "|")
            print("| STRENGTH: ", str(totalstr)[:5].ljust(5), "              |")
            print("| DIGESTION: ", str(totaldig)[:5].ljust(5), "             |")
            print("| HOSTILITY: ", str(totalhost[0]/overallhost)[:5].ljust(5), str(totalhost[1]/overallhost)[:5].ljust(5) , "       |")
            if overallfly > 0:
                print("| LAND/FLY: ", str(totalfly[0]/overallfly)[:5].ljust(5), str(totalfly[1]/overallfly)[:5].ljust(5) , "        |")
                print("| FLY STAT: ", str(totalbonus)[:5].ljust(5), "              |")
            print("| BUG COUNT: ",str(total).ljust(5) , "             |")
