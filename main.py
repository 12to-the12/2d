import pygame
import random
import math
import numpy as np
import os
#import noise


def clr(): os.system('cls')

clr()

def floor(x):
    return math.floor(x), x-math.floor(x)

def ceil(x):
    return math.ceil(x), math.ceil(x)-x

def zerotiny(x):
    if abs(x)<1e-2: return 0
    return x
pygame.init()
h_res, v_res = 1000,500
res = 100 # pixels per meter
surface = pygame.display.set_mode((h_res, v_res))
view_x, view_y = 50,50 # the center of the screen is 50 meters down and right of the top left of the field
# each block is 100 pixels wide, 100 pixels to the meter

clock = pygame.time.Clock()

alert_flag = True
def alert(message,*args):
    if alert_flag:
        print(message)
        for x in args: print(x)



class Block():
    def __init__(self):
        self.color = random.choice([(255,255,0),(255,0,255),(0,255,255)])

class World():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.generate()
        
        self.dimensions = self.array.shape
        alert(f'dimensions:{self.dimensions}')
    def generate(self):
        self.array = []
        alert("generating...")
        for y in range(self.x):
            row = []
            for x in range(self.y):
                chance = random.random()*0.04+1+y/self.y#+math.sin(0.1*x)
                chance = round(chance)
                if chance>1:row.append(1)
                else:row.append(0)
            self.array.append(row)
        alert("generated")
        self.array = np.array(self.array)
        print(type(self.array))



        alert('generated')

world = World(100,100)

h_blocks = h_res/res # each block is 100 pixels across, this computes the vertical number of blocks
v_blocks = v_res/res
alert(f"h and v blocks:{h_blocks},{v_blocks}")




colors = {
    0:(37,150,190), # sky
    1:(0,204,0), # earth
    2:(0,0,255)
}
acceleration = 0.3
x_acc, y_acc = 0,0
while True:
    
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                y_acc -= acceleration
            if event.key == pygame.K_s:
                y_acc += acceleration
            if event.key == pygame.K_a:
                x_acc -= acceleration
            if event.key == pygame.K_d:
                x_acc += acceleration

    view_x += x_acc
    view_y += y_acc
    #clr()
    print(x_acc)

    x_acc *= 0.9
    y_acc *= 0.9

    x_acc = zerotiny(x_acc)
    y_acc = zerotiny(y_acc)

    if view_x + h_blocks/2 > world.dimensions[0]:
        alert(f'over right boundary {view_x}')
        view_x = world.dimensions[0] - h_blocks/2
        alert(view_x)
    if view_x - h_blocks/2 < 0:
        alert(f'over left boundary {view_x}')
        view_x = 0 + h_blocks/2
        alert(view_x)
    if view_y + v_blocks/2 > world.dimensions[1]:
        alert(f'over bottom boundary {view_y}')
        view_y = world.dimensions[1] - v_blocks/2
        alert(view_y)
    if view_y - v_blocks/2 < 0:
        alert(f'over top boundary {view_y}')
        view_y = 0 + v_blocks/2
        alert(view_y)
        


    # Do logical updates here.
    # ...

    surface.fill("black")  # Fill the display with a solid color
    # Render the graphics here.
    # ...

    left, left_hang = floor(view_x-h_blocks/2)
    #alert(f"{view_x}-{h_blocks}/2")
    right, right_hang = ceil(view_x+h_blocks/2)
    top, top_hang = floor(view_y-v_blocks/2)
    bottom, bottom_hang = ceil(view_y+v_blocks/2)
    relevant = world.array[top:bottom+1, left:right+1]

    for i, row in enumerate(relevant):
        for j, item in enumerate(row):
            rectangle = pygame.Rect((      (j-left_hang)*res, (i-top_hang)*res    ), (res, res))
            pygame.draw.rect(surface, colors[item], rectangle)


    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)