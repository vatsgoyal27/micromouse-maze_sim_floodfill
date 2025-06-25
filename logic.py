
class FloodFillMap:
    def __init__(self, grid, goal_cells):
        self.grid = []
        for r in range(18):
            row = []
            for c in range(18):
                x, y, _ = grid[r][c]
                walls = ""
                if r == 0:
                    walls += "n"
                if r == 17:
                    walls += "s"
                if c == 0:
                    walls += "w"
                if c == 17:
                    walls += "e"
                row.append((x, y, walls))
            self.grid.append(row)

        #print(self.grid)
        self.goal = goal_cells
        self.cost_map = [[255 for _ in range(18)] for _ in range(18)]
        self.generate_cost_map()
        self.explored = [[False for _ in range(18)] for _ in range(18)]
        self.path = []


    def generate_cost_map(self):

        self.cost_map = [[255 for _ in range(18)] for _ in range(18)]

        queue = []
        for goal_cell in self.goal:
            r, c = goal_cell
            self.cost_map[r][c] = 0
            queue.append([r, c])

        while queue:
            r, c = queue.pop(0)  # Pop from front for BFS
            current_cost = self.cost_map[r][c]
            _, _, walls = self.grid[r][c]

            directions = {
                'n': (-1, 0),
                's': (1, 0),
                'e': (0, 1),
                'w': (0, -1)
            }

            for dir_key, (dr, dc) in directions.items():
                if dir_key not in walls:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 18 and 0 <= nc < 18:
                        if self.cost_map[nr][nc] > current_cost + 1:
                            self.cost_map[nr][nc] = current_cost + 1
                            queue.append((nr, nc))
        #self.print_map()

    def check_done(self, current_pos):
        all_explored = True
        all_unreachable = True
        xc, yc = current_pos[0], current_pos[1]
        for r in range(18):
            for c in range(18):
                if not self.explored[r][c]:
                    all_explored = False
                    if self.cost_map[r][c] != 255:
                        all_unreachable = False

        return (all_explored or all_unreachable) and (current_pos == [17, 0])

    def mark_explored(self, r, c):
        if 0 <= r < 18 and 0 <= c < 18:
            self.explored[r][c] = True

    def update_grid(self, cell_pos, walls):
        r, c = cell_pos
        x, y, _ = self.grid[r][c]
        existing_walls = self.grid[r][c][2]
        for w in walls:
            if w not in existing_walls:
                existing_walls += w
        self.grid[r][c] = (x, y, existing_walls)

        # Add opposite wall to neighbors manually
        if 'n' in walls and r > 0:
            rx, ry, rwalls = self.grid[r - 1][c]
            if 's' not in rwalls:
                self.grid[r - 1][c] = (rx, ry, rwalls + 's')

        if 's' in walls and r < 17:
            rx, ry, rwalls = self.grid[r + 1][c]
            if 'n' not in rwalls:
                self.grid[r + 1][c] = (rx, ry, rwalls + 'n')

        if 'e' in walls and c < 17:
            rx, ry, rwalls = self.grid[r][c + 1]
            if 'w' not in rwalls:
                self.grid[r][c + 1] = (rx, ry, rwalls + 'w')

        if 'w' in walls and c > 0:
            rx, ry, rwalls = self.grid[r][c - 1]
            if 'e' not in rwalls:
                self.grid[r][c - 1] = (rx, ry, rwalls + 'e')

        #print(self.grid)
        self.generate_cost_map()

    def explore(self, current_pos):
        r, c = current_pos[0], current_pos[1]

        self.mark_explored(r, c)  # Always mark current cell first

        # Check north
        if r > 0 and 'n' not in self.grid[r][c][2] and not self.explored[r-1][c]:
            self.path.append([r, c])
            return [r-1, c]
        # Check south
        if r < 17 and 's' not in self.grid[r][c][2] and not self.explored[r+1][c]:
            self.path.append([r, c])
            return [r+1, c]
        # Check east
        if c < 17 and 'e' not in self.grid[r][c][2] and not self.explored[r][c+1]:
            self.path.append([r, c])
            return [r, c+1]
        # Check west
        if c > 0 and 'w' not in self.grid[r][c][2] and not self.explored[r][c-1]:
            self.path.append([r, c])
            return [r, c-1]

        # Backtrack if all neighbors are explored or blocked
        if self.path:
            prev = self.path.pop()
            return prev
        else:
            return [r, c]  # Stay in place if no path to backtrack


    def get_next_cell(self, current_pos):
        r, c = current_pos[0], current_pos[1]
        current_cost = self.cost_map[r][c]

        directions = {
            'n': (-1, 0),
            's': (1, 0),
            'e': (0, 1),
            'w': (0, -1)
        }

        lowest_cost = current_cost
        next_cell = [r, c]  # Default: stay in place if no lower neighbor found

        for direction, (dr, dc) in directions.items():
            if direction not in self.grid[r][c][2]:  # No wall in this direction
                nr, nc = r + dr, c + dc
                if 0 <= nr < 18 and 0 <= nc < 18:
                    neighbor_cost = self.cost_map[nr][nc]
                    if neighbor_cost < lowest_cost:
                        lowest_cost = neighbor_cost
                        next_cell = [nr, nc]
        #print(next_cell)
        return next_cell

    def get_next_cell_backtrack(self, current_pos):
        r, c = current_pos[0], current_pos[1]
        current_cost = self.cost_map[r][c]

        directions = {
            'n': (-1, 0),
            's': (1, 0),
            'e': (0, 1),
            'w': (0, -1)
        }

        highest_cost = current_cost
        next_cell = [r, c]  # Default: stay in place if no higher neighbor found

        for direction, (dr, dc) in directions.items():
            if direction not in self.grid[r][c][2]:  # No wall in this direction
                nr, nc = r + dr, c + dc
                if 0 <= nr < 18 and 0 <= nc < 18:
                    neighbor_cost = self.cost_map[nr][nc]
                    if neighbor_cost > highest_cost:
                        highest_cost = neighbor_cost
                        next_cell = [nr, nc]
        print(next_cell)
        return next_cell

    def get_next_cell_actual(self, current_pos):
        r, c = current_pos[0], current_pos[1]
        current_cost = self.cost_map[r][c]

        directions = {
            'n': (-1, 0),
            's': (1, 0),
            'e': (0, 1),
            'w': (0, -1)
        }

        lowest_cost = current_cost
        next_cell = [r, c]  # Default to current cell

        for direction, (dr, dc) in directions.items():
            if direction not in self.grid[r][c][2]:  # No wall in this direction
                nr, nc = r + dr, c + dc
                if 0 <= nr < 18 and 0 <= nc < 18:
                    neighbor_cost = self.cost_map[nr][nc]
                    if neighbor_cost < lowest_cost:
                        lowest_cost = neighbor_cost
                        next_cell = [nr, nc]

        is_explored = self.explored[r][c]  # Status of current cell
        return next_cell, is_explored

    def print_map(self):
        for row in self.cost_map:
            print(" ".join(f"{val:3}" for val in row))
        print("--------------------------------------------------")
