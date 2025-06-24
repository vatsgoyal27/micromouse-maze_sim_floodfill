# Create grid with all walls (n, e, s, w)
grid = [[(x, y, "nesw") for x in range(30, 381, 20)] for y in range(370, 29, -20)]

def remove_wall(gridp, row, col, direction):
    x, y, walls = gridp[row][col]
    walls = walls.replace(direction, "")
    gridp[row][col] = (x, y, walls)

def remove_wall_bidirectional(gridp, row, col, direction):
    remove_wall(gridp, row, col, direction)
    delta = {
        'n': (-1, 0, 's'),
        's': (1, 0, 'n'),
        'e': (0, 1, 'w'),
        'w': (0, -1, 'e')
    }
    if direction in delta:
        dr, dc, opposite = delta[direction]
        nr, nc = row + dr, col + dc
        if 0 <= nr < 18 and 0 <= nc < 18:
            remove_wall(gridp, nr, nc, opposite)

# --- MAIN PATH (ZIG-ZAG from bottom-left to top-right) ---
path = [(17, 0)]
# Vertical up
for r in range(16, 10, -1):
    path.append((r, 0))
# Right
for c in range(1, 5):
    path.append((10, c))
# Up
for r in range(9, 6, -1):
    path.append((r, 4))
# Right
for c in range(5, 10):
    path.append((6, c))
# Up
for r in range(5, 2, -1):
    path.append((r, 9))
# Right
for c in range(10, 14):
    path.append((2, c))
# Up
for r in range(1, -1, -1):
    path.append((r, 13))
# Right to (0,17)
for c in range(14, 18):
    path.append((0, c))

for i in range(len(path) - 1):
    r1, c1 = path[i]
    r2, c2 = path[i + 1]
    if r2 < r1:
        remove_wall_bidirectional(grid, r1, c1, 'n')
    elif r2 > r1:
        remove_wall_bidirectional(grid, r1, c1, 's')
    elif c2 < c1:
        remove_wall_bidirectional(grid, r1, c1, 'w')
    elif c2 > c1:
        remove_wall_bidirectional(grid, r1, c1, 'e')

    #fixing chat gpts map generation
    remove_wall_bidirectional(grid, 10, 0, 'e')
    remove_wall_bidirectional(grid, 6, 4, 'e')
    remove_wall_bidirectional(grid, 3, 11, 'n')

# --- FALSE PATHS / DEAD ENDS ---

# Random dead-end vertical shaft from (13, 2)
for r in range(13, 10, -1):
    remove_wall_bidirectional(grid, r, 2, 'n')

# False horizontal from (6, 11) to (6, 15)
for c in range(11, 16):
    remove_wall_bidirectional(grid, 6, c, 'e')

# False vertical from (9, 5) to (5, 5)
for r in range(9, 5, -1):
    remove_wall_bidirectional(grid, r, 5, 'n')

# Backtracking loop near start
remove_wall_bidirectional(grid, 17, 0, 'e')
remove_wall_bidirectional(grid, 17, 1, 'e')
remove_wall_bidirectional(grid, 17, 2, 'n')
remove_wall_bidirectional(grid, 16, 2, 'w')
remove_wall_bidirectional(grid, 16, 1, 's')

# Trap path from (2, 14) down to (5, 14)
for r in range(2, 6):
    remove_wall_bidirectional(grid, r, 14, 's')

# Small loop near (7, 7)
remove_wall_bidirectional(grid, 7, 7, 'e')
remove_wall_bidirectional(grid, 7, 8, 's')
remove_wall_bidirectional(grid, 8, 8, 'w')
remove_wall_bidirectional(grid, 8, 7, 'n')

# Small false fork from (3, 9)
remove_wall_bidirectional(grid, 3, 9, 'e')
remove_wall_bidirectional(grid, 3, 10, 'e')

# Complex false zig-zag from (15, 5)
remove_wall_bidirectional(grid, 15, 5, 'n')
remove_wall_bidirectional(grid, 14, 5, 'e')
remove_wall_bidirectional(grid, 14, 6, 'n')
remove_wall_bidirectional(grid, 13, 6, 'e')
remove_wall_bidirectional(grid, 13, 7, 's')

# Done
