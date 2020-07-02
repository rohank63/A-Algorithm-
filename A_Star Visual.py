import math
import pygame
from tkinter import *
from tkinter import ttk

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Rohan - A* Star")


class Spot:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbours = []
        self.previous = None
        self.obs = False

    def show(self, color, st):
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
        pygame.display.update()

    def path(self, color, st):
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
        pygame.display.update()

    def add_neighbours(self, grid):
        i = self.i
        j = self.j
        if i < cols-1 and grid[i + 1][j].obs is False:
            self.neighbours.append(grid[i + 1][j])
        if i > 0 and grid[i - 1][j].obs is False:
            self.neighbours.append(grid[i - 1][j])
        if j < rows-1 and grid[i][j + 1].obs is False:
            self.neighbours.append(grid[i][j + 1])
        if j > 0 and grid[i][j - 1].obs is False:
            self.neighbours.append(grid[i][j - 1])
        if i > 0 and j > 0 and grid[i-1][j-1].obs is False and grid[i][j-1].obs is False and grid[i-1][j].obs is False:
            self.neighbours.append(grid[i-1][j-1])
        if i < cols-1 and j > 0 and grid[i+1][j-1].obs is False and grid[i][j-1].obs is False and grid[i+1][j].obs is False:
            self.neighbours.append(grid[i+1][j-1])
        if i > 0 and j < rows-1 and grid[i-1][j+1].obs is False and grid[i-1][j].obs is False and grid[i][j+1].obs is False:
            self.neighbours.append(grid[i-1][j+1])
        if i < cols-1 and j < rows-1 and grid[i+1][j+1].obs is False and grid[i+1][j].obs is False and grid[i][j+1].obs is False:
            self.neighbours.append(grid[i+1][j+1])


cols = 50
rows = 50
grid = [0 for i in range(cols)]
open_set = []
closed_set = []
red = (255, 0, 0)
olive = (52, 254, 217)
grey = (220, 220, 220)
white = (255, 255, 255)
yellow = (255, 255, 0)
blue = (0, 0, 255)
green = (44, 220, 42)
w = 500 / cols
h = 500 / rows

for i in range(cols):
    grid[i] = [0 for j in range(rows)]


for i in range(cols):
    for j in range(rows):
        grid[i][j] = Spot(i, j)

start = grid[5][5]
end = grid[40][40]

# Dipslay Grid
for i in range(cols):
    for j in range(rows):
        grid[i][j].show(white, 1)

# Coloring Grey
for i in range(0, rows):
    grid[0][i].show(grey, 0)
    grid[0][i].obs = True
    grid[cols-1][i].show(grey, 0)
    grid[cols-1][i].obs = True
    grid[i][0].show(grey, 0)
    grid[i][0].obs = True
    grid[i][rows-1].show(grey, 0)
    grid[i][rows-1].obs = True


# Submit Function
def on_submit():
    global start
    global end
    st = start_box.get().split(',')
    ed = end_box.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()


window = Tk()
window.geometry("200x110")
window.title("Coordinates")
window.config(background="black")
start_label = Label(window, text="Start(x,y): ")
start_box = Entry(window)
start_box.focus()
end_label = Label(window, text="End(x,y): ")
end_box = Entry(window)
var = IntVar()
show_path = ttk.Checkbutton(window, text="Show Path", onvalue=1, offvalue=0, variable=var)
submit = Button(window, text="Submit", command=on_submit)

start_label.grid(row=0, column=0, pady=5, padx=5)
start_box.grid(row=0, column=1, pady=5)
end_label.grid(row=1, column=0, pady=5, padx=5)
end_box.grid(row=1, column=1, pady=5)
show_path.grid(row=2, columnspan=2)
submit.grid(row=3, columnspan=2)

window.update()
window.mainloop()

pygame.init()
open_set.append(start)


start.show(yellow, 0)
end.show(yellow, 0)


def mouse_press(x):
    x_cod = x[0]
    y_cod = x[1]
    g1 = x_cod // (500 // cols)
    g2 = y_cod // (500 // rows)
    point = grid[g1][g2]
    if point != start and point != end:
        if point.obs is False:
            point.obs = True
            point.show(olive, 0)


loop = True
while loop:
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mouse_press(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                loop = False
                break

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbours(grid)


def heuristic(n, e):
    dis = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2)
    return dis


def main():
    while True:
        if len(open_set) > 0:
            lowest_index = 0
            for i in range(len(open_set)):
                if open_set[i].f < open_set[lowest_index].f:
                    lowest_index = i

            current = open_set[lowest_index]

            if current == end:
                print('Done', current.f)
                while current.previous:
                    current.show(blue, 0)
                    current = current.previous
                current.show(blue, 0)
                break

            open_set.pop(lowest_index)
            closed_set.append(current)
            ########
            if var.get():
            	current.show(red, 0)
            ########
            neighbours = current.neighbours
            for i in range(len(neighbours)):
                neighbour = neighbours[i]
                if neighbour not in closed_set:
                    tempG = current.g + 1
                    check = False
                    if neighbour in open_set:
                        if neighbour.g > tempG:
                            check = True
                            neighbour.g = tempG
                    else:
                        neighbour.g = tempG
                        check = True
                        open_set.append(neighbour)
                        #####
                        if var.get():
                        	neighbour.show(green, 0)
                        #####
                    if check:
                        neighbour.h = heuristic(neighbour, end)
                        neighbour.f = neighbour.g + neighbour.h
                        neighbour.previous = current

        else:
            print("No Solution")
            break
        # Show Visualization
        '''if var.get():
            for i in range(len(open_set)):
                open_set[i].show(green, 0)
            for i in range(len(closed_set)):
                closed_set[i].show(red, 0)'''


if __name__ == "__main__":
    main()

    while True:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
