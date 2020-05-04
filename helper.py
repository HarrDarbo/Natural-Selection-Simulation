import string

from food import Food

def init():
    # other
    global canvas
    canvas = None
    global clen
    clen = 300

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
        bug.attack(enemy)

def killbug(bug):
    bugs.remove(bug)
    buggrid[int(bug.x+.5)-1][int(bug.y+.5)-1].remove(bug)
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

def statistics():
    totalstr = 0
    totalm = [0,0,0,0]
    totalp = [0,0,0,0]
    for bug in bugs:
        totalstr+=bug.strength
        for n in range(4):
            totalm[n] += bug.moves[n]
            totalp[n] += bug.movechance[n]
    totalstr = totalstr / len(bugs)
    for n in range(4):
        totalm[n] = totalm[n] / len(bugs)
        totalp[n] = totalp[n] / len(bugs)
    overallp = totalp[0] + totalp[1] + totalp[2] + totalp[3]
    print("============AVGSTATS==============")
    print("|        NORTH SOUTH EAST  WEST  |")
    print("| PROB: ", str(totalp[0]/overallp)[:5].ljust(5), str(totalp[1]/overallp)[:5].ljust(5), str(totalp[2]/overallp)[:5].ljust(5), str(totalp[3]/overallp)[:5].ljust(5), "|")
    print("| DIST: ", str(totalm[0])[:5].ljust(5), str(totalm[1])[:5].ljust(5), str(totalm[2])[:5].ljust(5), str(totalm[3])[:5].ljust(5)    , "|")
    print("| STRENGTH: ",str(totalstr)[:5].ljust(5) , "              |")
    print("| BUG COUNT: ",str(len(bugs)).ljust(5) , "             |")
