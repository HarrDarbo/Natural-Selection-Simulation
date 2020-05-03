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
        buggrid.append([[]]*clen)

    # Food Tracking
    global foods
    foods = list()
    global foodgrid
    foodgrid = []
    for n in range(clen):
        foodgrid.append([0]*clen)

def makebug(bug):
    bugs.append(bug)
    buggrid[int(bug.x)][int(bug.y)].append(bug)

def movebug(bug):
    pass

def attackbug():
    pass

def kilbug():
    pass

def makefood():
    food = Food()
    foods.append(food)
    foodgrid[int(food.x)][int(food.y)] += 1

def eatfood(x, y):
    foodamt = foodgrid[x][y]
    foodgrid[x][y] = 0
    if foodamt > 0:
        for food in foods:
            if int(food.x) == x and int(food.y) == y:
                foods.remove(food)
    return foodamt

def statistics():
    totalstr = 0
    totalm = [0,0,0,0]
    for bug in bugs:
        totalstr+=bug.strength
        for n in range(4):
            totalm[n] += bug.moves[n]
    totalstr = totalstr / len(bugs)
    for n in range(4):
        totalm[n] = totalm[n] / len(bugs)
    print(totalm[0], totalm[1], totalm[2], totalm[3])
    print(totalstr)
