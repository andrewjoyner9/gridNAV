GRID_SIZE = 10  # Change this to adjust the grid size
BLOCKING_TYPES = ["tree", "no_fly_zone", "building_edge", "adversarial_drone"] # Define blocking types

# Define obstacles positions directly
obstacles = [
    (2, 2, "tree"),
    (6, 9, "no_fly_zone"),
    (1, 4, "building_edge"),
    (5, 7, "adversarial_drone")
]

def print_grid(grid, path, size): # Function to print grid out in the console
    symbol_map = {
        "start": "S",
        "end": "E",
        "tree": "#",
        "no_fly_zone": "X",
        "building_edge": "B",
        "adversarial_drone": "D"
    }

    for y in range(size): 
        row = ""
        for x in range(size):
            pos = (x, y)
            if pos in path and pos not in [path[0], path[-1]]: # Check if the position is in the path that the logic took and also not the start or end
                row += "* "
            elif pos in grid:
                row += symbol_map.get(grid[pos], "?") # Get the relevaant symbol for the grid position
            else:
                row += ". "
        print(row)


start = (0, 0, "start") # Define start position
end = (5, 9, "end") # Define end position

# Build grid as a dict: (x, y) -> type
grid = {}
for x, y, typ in obstacles:
    grid[(x, y)] = typ
grid[(start[0], start[1])] = "start"
grid[(end[0], end[1])] = "end"

# Assign (x, y) positions
x, y = start[0], start[1]
target_x, target_y = end[0], end[1]

path = []

while (x, y) != (target_x, target_y):
    path.append((x, y))

    # Step toward target
    dx = 1 if x < target_x else -1 if x > target_x else 0 # This allows the drone to move diagonally if needed
    dy = 1 if y < target_y else -1 if y > target_y else 0

    next_x = x + dx 
    next_y = y + dy

    obstacle = grid.get((next_x, next_y), None) # Checks if next position is blocked by an obstacle

    if obstacle in BLOCKING_TYPES:
        # Try to sidestep right first
        if grid.get((x + 1, y)) not in BLOCKING_TYPES and x + 1 < GRID_SIZE:
            x += 1
        elif grid.get((x - 1, y)) not in BLOCKING_TYPES and x - 1 >= 0:
            x -= 1
        else:
            print(f"Blocked at {(x, y)} by '{obstacle}'. No sidestep possible.")
            break
    else:
        x, y = next_x, next_y

path.append((x, y))  # Include final position this iteration

# Show path
print("Path:")
for step in path:
    label = grid.get(step, "")
    print(f"{step} {f'({label})' if label else ''}")

print("\nGrid:")
print_grid(grid, path, GRID_SIZE)
