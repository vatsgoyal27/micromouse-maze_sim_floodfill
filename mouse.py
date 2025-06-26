from turtle import Turtle

class Mouse():
    def __init__(self):
        self.create_mouse()
        self.mouse_pos = [17,0]
        self.mouse.width(1)

    def create_mouse(self):
        self.mouse = Turtle(shape='square')
        self.mouse.setheading(90)
        #self.mouse.shapesize(0.5, 0.5)
        self.mouse.hideturtle()
        self.mouse.penup()
        self.mouse.goto(30, 30)
        self.mouse.pendown()
        self.mouse.showturtle()
        self.mouse.speed(6)

    def draw_grid(self):
        self.mouse.hideturtle()
        self.mouse.speed(0)
        self.mouse.penup()
        self.mouse.pencolor("black")
        self.mouse.width(1)

        # Draw vertical lines
        for x in range(20, 381, 20):
            self.mouse.goto(x, 20)
            self.mouse.setheading(90)
            self.mouse.pendown()
            self.mouse.forward(360)
            self.mouse.penup()

        # Draw horizontal lines
        for y in range(20, 381, 20):
            self.mouse.goto(20, y)
            self.mouse.setheading(0)
            self.mouse.pendown()
            self.mouse.forward(360)
            self.mouse.penup()

    def draw_walls(self, grid):
        self.mouse.hideturtle()
        self.mouse.speed(0)
        self.mouse.penup()
        self.mouse.pencolor("red")
        self.mouse.width(2)

        cell_size = 20

        for row in range(18):
            for col in range(18):
                x, y, walls = grid[row][col]

                if 'n' in walls:
                    self.mouse.goto(x - cell_size // 2, y + cell_size // 2)
                    self.mouse.setheading(0)
                    self.mouse.pendown()
                    self.mouse.forward(cell_size)
                    self.mouse.penup()

                if 'e' in walls:
                    self.mouse.goto(x + cell_size // 2, y + cell_size // 2)
                    self.mouse.setheading(-90)
                    self.mouse.pendown()
                    self.mouse.forward(cell_size)
                    self.mouse.penup()

                if 's' in walls:
                    self.mouse.goto(x + cell_size // 2, y - cell_size // 2)
                    self.mouse.setheading(180)
                    self.mouse.pendown()
                    self.mouse.forward(cell_size)
                    self.mouse.penup()

                if 'w' in walls:
                    self.mouse.goto(x - cell_size // 2, y - cell_size // 2)
                    self.mouse.setheading(90)
                    self.mouse.pendown()
                    self.mouse.forward(cell_size)
                    self.mouse.penup()

    def delete(self):
        self.mouse.penup()
        self.mouse.hideturtle()

    def f(self):
        heading = self.mouse.heading()

        if heading == 90:  # North
            self.mouse_pos[0] -= 1
            self.mouse.forward(20)
        elif heading == 0:  # East
            self.mouse_pos[1] += 1
            self.mouse.forward(20)
        elif heading == 180:  # West
            self.mouse_pos[1] -= 1
            self.mouse.forward(20)
        elif heading == 270:  # South
            self.mouse_pos[0] += 1
            self.mouse.forward(20)
        elif heading == 45:  # North-East
            self.mouse_pos[0] -= 1
            self.mouse_pos[1] += 1
            self.mouse.forward(28.28)
        elif heading == 135:  # North-West
            self.mouse_pos[0] -= 1
            self.mouse_pos[1] -= 1
            self.mouse.forward(28.28)
        elif heading == 225:  # South-West
            self.mouse_pos[0] += 1
            self.mouse_pos[1] -= 1
            self.mouse.forward(28.28)
        elif heading == 315:  # South-East
            self.mouse_pos[0] += 1
            self.mouse_pos[1] += 1
            self.mouse.forward(28.28)

    def dir(self):
        return self.mouse.heading()

    def reset(self):
        self.mouse_pos = [17, 0]
        self.mouse.pencolor('blue')
        self.mouse.width(6)
        self.mouse.speed(1)

    def move_explore(self, to):
        nx, ny = to[0], to[1]
        cx, cy = self.mouse_pos[0], self.mouse_pos[1]
        if nx< cx:
            self.mouse.setheading(90)
            self.f()
        if nx> cx:
            self.mouse.setheading(270)
            self.f()
        if ny < cy:
            self.mouse.setheading(180)
            self.f()
        if ny > cy:
            self.mouse.setheading(0)
            self.f()

    def move_dia(self, to):
        nx, ny = to[0], to[1]
        cx, cy = self.mouse_pos[0], self.mouse_pos[1]
        dx = nx - cx
        dy = ny - cy

        if dx == -1 and dy == 0:
            self.mouse.setheading(90)  # North
        elif dx == 1 and dy == 0:
            self.mouse.setheading(270)  # South
        elif dx == 0 and dy == -1:
            self.mouse.setheading(180)  # West
        elif dx == 0 and dy == 1:
            self.mouse.setheading(0)  # East
        elif dx == -1 and dy == 1:
            self.mouse.setheading(45)  # North-East
        elif dx == 1 and dy == 1:
            self.mouse.setheading(315)  # South-East
        elif dx == 1 and dy == -1:
            self.mouse.setheading(225)  # South-West
        elif dx == -1 and dy == -1:
            self.mouse.setheading(135)  # North-West
        self.f()

    def move_p_con(self, segment):
        _, ang, steps = segment
        scaled_speed = min(10, max(1, steps))  # Clamp to range [1, 10]
        self.mouse.speed(scaled_speed)
        self.mouse.setheading(ang)
        for i in range(steps):
            self.f()

