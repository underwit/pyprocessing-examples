import random
from itertools import product


CS = 10  # cell size
W = 600  # width
H = 600  # height
COLS = W // CS
ROWS = H // CS
DENSITY = 0.35
dirs = list(product((-1, 0, 1), repeat=2))
dirs.remove((0, 0))
points = []
new_points = []
run = False


def xy2flat(x, y):
    x = (x + COLS) % COLS
    y = (y + ROWS) % ROWS
    return x + COLS * y


def flat2xy(index):
    return index % COLS, index // COLS


def setup():
    frameRate(20)
    size(600, 600)
    for i in range(0, W * H, CS):
        points.append(random.random() < DENSITY)
        new_points.append(False)


def mouseClicked():
    x = mouseX // CS
    y = mouseY // CS
    index = xy2flat(x, y)
    points[index] = not points[index]


def keyPressed():
    global run
    if key == ' ':
        run = not run
    elif key == 'r':  # randomly fill the board
        for i, _ in enumerate(points):
            points[i] = random.random() < DENSITY
    elif key == 'c':  # clear the board
        for i, _ in enumerate(points):
            points[i] = False


def calc_cell(index):
    x, y = flat2xy(index)
    nb = sum([points[xy2flat(x + _x, y + _y)] for _x, _y in dirs])
    new_points[index] = points[index]
    if points[index] and (nb < 2 or nb > 3):
        new_points[index] = False
    elif nb == 3:
        new_points[index] = True


def draw():
    global points, new_points
    background(52, 63, 62)
    fill(220, 237, 255)
    for index, is_alive in enumerate(points):
        if is_alive:
            x, y = flat2xy(index)
            rect(x * CS, y * CS, CS, CS)
        if run:
            calc_cell(index)
    if run:
        points, new_points = new_points, points
