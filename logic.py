
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
        self.final_path = []


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


    # def get_next_cell(self, current_pos):
    #     r, c = current_pos[0], current_pos[1]
    #     current_cost = self.cost_map[r][c]
    #
    #     directions = {
    #         'n': (-1, 0),
    #         's': (1, 0),
    #         'e': (0, 1),
    #         'w': (0, -1)
    #     }
    #
    #     lowest_cost = current_cost
    #     next_cell = [r, c]  # Default: stay in place if no lower neighbor found
    #
    #     for direction, (dr, dc) in directions.items():
    #         if direction not in self.grid[r][c][2]:  # No wall in this direction
    #             nr, nc = r + dr, c + dc
    #             if 0 <= nr < 18 and 0 <= nc < 18:
    #                 neighbor_cost = self.cost_map[nr][nc]
    #                 if neighbor_cost < lowest_cost:
    #                     lowest_cost = neighbor_cost
    #                     next_cell = [nr, nc]
    #     #print(next_cell)
    #     return next_cell

    def get_final_path(self, ini_pos):
        r, c = ini_pos
        path = [[r, c]]  # Start from initial position

        while [r, c] not in self.goal:
            current_cost = self.cost_map[r][c]
            lowest_cost = current_cost
            next_cell = [r, c]

            for direction, (dr, dc) in {
                'n': (-1, 0), 's': (1, 0), 'e': (0, 1), 'w': (0, -1)
            }.items():
                if direction not in self.grid[r][c][2]:  # No wall
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 18 and 0 <= nc < 18:
                        if self.cost_map[nr][nc] < lowest_cost:
                            lowest_cost = self.cost_map[nr][nc]
                            next_cell = [nr, nc]

            if next_cell == [r, c]:  # No progress, stuck
                break

            path.append(next_cell)
            r, c = next_cell

        return path

    def process_path_1(self, path):
        if len(path) < 3:
            return path[:]

        new_path = [path[0]]

        i = 0
        while i < len(path) - 2:
            a = path[i]  # start
            b = path[i + 1]  # middle (possible L-turn)
            c = path[i + 2]  # end

            # Check if b is an L-turn vertex:
            # a→b and b→c are perpendicular
            dx1, dy1 = b[0] - a[0], b[1] - a[1]
            dx2, dy2 = c[0] - b[0], c[1] - b[1]

            # if directions form 90 degrees (dot product == 0)
            if dx1 * dx2 + dy1 * dy2 == 0:
                # skip the middle vertex (b)
                new_path.append(c)
                i += 2  # skip over b
            else:
                new_path.append(b)
                i += 1

        # Add last point if missed
        if new_path[-1] != path[-1]:
            new_path.append(path[-1])

        return new_path

    def process_path_2(self, path):
        processed = []
        if len(path) < 2:
            return path

        def get_heading(dxx, dyy):
            if dxx == -1 and dyy == 0: return 90
            if dxx == -1 and dyy == 1: return 45
            if dxx == 0 and dyy == 1: return 0
            if dxx == 1 and dyy == 1: return 315
            if dxx == 1 and dyy == 0: return 270
            if dxx == 1 and dyy == -1: return 225
            if dxx == 0 and dyy == -1: return 180
            if dxx == -1 and dyy == -1: return 135
            return None

        i = 0
        while i < len(path) - 1:
            start = path[i]
            dxx = path[i + 1][0] - start[0]
            dyy = path[i + 1][1] - start[1]
            heading = get_heading(dxx, dyy)
            steps = 1
            j = i + 1

            while j < len(path) - 1:
                next_dx = path[j + 1][0] - path[j][0]
                next_dy = path[j + 1][1] - path[j][1]
                if get_heading(next_dx, next_dy) == heading:
                    steps += 1
                    j += 1
                else:
                    break

            processed.append((start, heading, steps))
            i = j

        return processed

    def print_map(self):
        for row in self.cost_map:
            print(" ".join(f"{val:3}" for val in row))
        print("--------------------------------------------------")
