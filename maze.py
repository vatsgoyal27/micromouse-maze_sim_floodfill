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

def add_wall_bidirectional(grid, row, col, direction):
    # Define direction deltas and opposites
    delta = {
        'n': (-1, 0, 's'),
        's': (1, 0, 'n'),
        'e': (0, 1, 'w'),
        'w': (0, -1, 'e')
    }

    if direction in delta:
        dr, dc, opposite = delta[direction]
        nr, nc = row + dr, col + dc

        # Add wall to the current cell
        x, y, walls = grid[row][col]
        if direction not in walls:
            walls += direction
            grid[row][col] = (x, y, walls)

        # Add wall to the neighboring cell
        if 0 <= nr < 18 and 0 <= nc < 18:
            x2, y2, neighbor_walls = grid[nr][nc]
            if opposite not in neighbor_walls:
                neighbor_walls += opposite
                grid[nr][nc] = (x2, y2, neighbor_walls)


# --------------------------
# 🔁 BUILD CONCENTRIC LOOPS
# --------------------------
layers = [
    (1, 16),  # outermost loop: rows 1-16, cols 1-16
    (3, 14),
    (5, 12),
    (6, 11),
    (7, 10)   # innermost loop
]

for layer in layers:
    r1, r2 = layer[0], layer[1]
    for c in range(r1, r2):   # top
        remove_wall_bidirectional(grid, r1, c, 'e')
    for r in range(r1, r2):   # right
        remove_wall_bidirectional(grid, r, r2, 's')
    for c in range(r2, r1, -1):  # bottom
        remove_wall_bidirectional(grid, r2, c, 'w')
    for r in range(r2, r1, -1):  # left
        remove_wall_bidirectional(grid, r, r1, 'n')

# --------------------------
# ❌ FAKE PATHS + DECOYS
# --------------------------

# Fake entry to layer 1
remove_wall_bidirectional(grid, 17, 1, 'n')
remove_wall_bidirectional(grid, 16, 1, 'n')
remove_wall_bidirectional(grid, 15, 1, 'e')
remove_wall_bidirectional(grid, 15, 2, 'e')
remove_wall_bidirectional(grid, 15, 3, 'n')
# Dead end

# Fork inside 2nd loop
remove_wall_bidirectional(grid, 4, 13, 's')
remove_wall_bidirectional(grid, 5, 13, 's')
remove_wall_bidirectional(grid, 6, 13, 'e')
remove_wall_bidirectional(grid, 6, 14, 'e')
# End

# Loop in middle
remove_wall_bidirectional(grid, 10, 8, 'w')
remove_wall_bidirectional(grid, 10, 7, 'n')
remove_wall_bidirectional(grid, 9, 7, 'e')
remove_wall_bidirectional(grid, 9, 8, 'n')
remove_wall_bidirectional(grid, 9, 8, 'e')

# Spiral trap
remove_wall_bidirectional(grid, 1, 14, 's')
remove_wall_bidirectional(grid, 2, 14, 'w')
remove_wall_bidirectional(grid, 2, 13, 's')
remove_wall_bidirectional(grid, 3, 13, 'w')
remove_wall_bidirectional(grid, 3, 12, 'n')

# Zigzag fork
remove_wall_bidirectional(grid, 11, 2, 'e')
remove_wall_bidirectional(grid, 11, 3, 'n')
remove_wall_bidirectional(grid, 10, 3, 'e')
remove_wall_bidirectional(grid, 10, 4, 'n')

# Extra fork near goal (deceptive)
remove_wall_bidirectional(grid, 7, 10, 'e')
remove_wall_bidirectional(grid, 7, 11, 'n')
remove_wall_bidirectional(grid, 6, 11, 'e')
remove_wall_bidirectional(grid, 6, 12, 's')

# Done!

remove_wall_bidirectional(grid, 17, 0, 'n')
remove_wall_bidirectional(grid, 17, 1, 'n')
remove_wall_bidirectional(grid, 17, 2, 'n')
remove_wall_bidirectional(grid, 17, 0, 'e')
remove_wall_bidirectional(grid, 6, 12, 'e')
remove_wall_bidirectional(grid, 8, 8, 'e')
remove_wall_bidirectional(grid, 8, 7, 'n')
remove_wall_bidirectional(grid, 9, 9, 'n')