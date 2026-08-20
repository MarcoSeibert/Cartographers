import random

class BoardModel:
    def __init__(self, grid_size=11):
        self.grid_size = grid_size
        self.grid_state = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        self.terrain_types = ["WA", "AC", "WS", "DO", "MO"]
        self.connected_terrain_types = ["WA", "WS", "AC", "DO"]

    def set_terrain(self, row, col, terrain_type):
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.grid_state[row][col] = terrain_type

    def find_connected_fields(self, row, col, terrain_type):
        if terrain_type not in self.connected_terrain_types:
            return {(row, col)}

        connected = set()
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            if (r, c) not in connected and 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                if self.grid_state[r][c] == terrain_type:
                    connected.add((r, c))
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        stack.append((r + dr, c + dc))
        return connected