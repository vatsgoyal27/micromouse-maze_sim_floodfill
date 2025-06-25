from turtle import tracer, Screen
from maze import grid
from logic import FloodFillMap
from mouse import Mouse
import time

screen = Screen()
screen.setworldcoordinates(0, 0, 400, 400)

tracer(0)
my_mouse = Mouse()
grid_mouse = Mouse()
grid_mouse.draw_grid()
grid_mouse.draw_walls(grid)
grid_mouse.delete()
screen.update()
tracer(1)

win_cells = [[8, 9],[9, 8], [9, 9], [8, 8]]
ff = FloodFillMap(grid, win_cells)

def check_sensors():
    # returns a vector [l, f, r] of simulated sensor readings
    sensor_reading = [0, 0, 0]
    direc = my_mouse.dir()
    if direc == 90:
        if 'n' in grid[my_mouse.mouse_pos[0]][my_mouse.mouse_pos[1]][2]:
            sensor_reading[1] = 1
        if 'e' in grid[my_mouse.mouse_pos[0]][my_mouse.mouse_pos[1]][2]:
            sensor_reading[2] = 1
        if 'w' in grid[my_mouse.mouse_pos[0]][my_mouse.mouse_pos[1]][2]:
            sensor_reading[0] = 1
    if direc == 0:
        if 'e' in grid[my_mouse.mouse_pos[0]][my_mouse.mouse_pos[1]][2]:
            sensor_reading[1] = 1
        if 's' in grid[my_mouse.mouse_pos[0]][my_mouse.mouse_pos[1]][2]:
            sensor_reading[2] = 1
        if 'n' in grid[my_mouse.mouse_pos[0]][my_mouse.mouse_pos[1]][2]:
            sensor_reading[0] = 1
    if direc == 180:
        if 'w' in grid[my_mouse.mouse_pos[0]][my_mouse.mouse_pos[1]][2]:
            sensor_reading[1] = 1
        if 'n' in grid[my_mouse.mouse_pos[0]][my_mouse.mouse_pos[1]][2]:
            sensor_reading[2] = 1
        if 's' in grid[my_mouse.mouse_pos[0]][my_mouse.mouse_pos[1]][2]:
            sensor_reading[0] = 1
    if direc == 270:
        if 's' in grid[my_mouse.mouse_pos[0]][my_mouse.mouse_pos[1]][2]:
            sensor_reading[1] = 1
        if 'w' in grid[my_mouse.mouse_pos[0]][my_mouse.mouse_pos[1]][2]:
            sensor_reading[2] = 1
        if 'e' in grid[my_mouse.mouse_pos[0]][my_mouse.mouse_pos[1]][2]:
            sensor_reading[0] = 1
    return sensor_reading_to_walls(sensor_reading, direc)

def sensor_reading_to_walls(sensor_reading, direc):
    walls = ""
    if direc == 90:
        if sensor_reading[0] == 1:
            walls += "w"
        if sensor_reading[1] == 1:
            walls += "n"
        if sensor_reading[2] == 1:
            walls += "e"
    if direc == 0:
        if sensor_reading[0] == 1:
            walls += "n"
        if sensor_reading[1] == 1:
            walls += "e"
        if sensor_reading[2] == 1:
            walls += "s"
    if direc == 180:
        if sensor_reading[0] == 1:
            walls += "s"
        if sensor_reading[1] == 1:
            walls += "w"
        if sensor_reading[2] == 1:
            walls += "n"
    if direc == 270:
        if sensor_reading[0] == 1:
            walls += "e"
        if sensor_reading[1] == 1:
            walls += "s"
        if sensor_reading[2] == 1:
            walls += "w"
    return walls

def win(pos_array):
    if pos_array in win_cells:
        return True
    else:
        return False

''' logic-mapping'''

while not ff.check_done():
    time.sleep(0.01)
    cx, cy = my_mouse.mouse_pos[0], my_mouse.mouse_pos[1]
    ff.update_grid(my_mouse.mouse_pos, check_sensors())
    next_move = ff.explore(my_mouse.mouse_pos)
    my_mouse.move_actual(next_move)

time.sleep(2)
my_mouse.reset()

'''logic-move! HAHAHAHHAHAHAHAHAHHAHA'''
while not win(my_mouse.mouse_pos):
    next_move= ff.get_next_cell(my_mouse.mouse_pos)
    my_mouse.move_actual(next_move)
    print(next_move)





screen.exitonclick()

