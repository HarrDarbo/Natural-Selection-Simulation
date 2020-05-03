from food import Food

def init():
    global bugs
    bugs = list()
    global canvas
    canvas = None
    global clen
    clen = 300
    global foods
    foods = list()
    global foodgrid
    foodgrid = []
    for n in range(clen):
        foodgrid.append([0]*clen)

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
