class BoardController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_terrain = "WA"

    def on_terrain_selected(self, terrain_type):
        self.current_terrain = terrain_type

    def on_canvas_click(self, event):
        col = event.x // self.view.cell_size
        row = event.y // self.view.cell_size
        if 0 <= row < self.model.grid_size and 0 <= col < self.model.grid_size:
            terrain_type = self.current_terrain
            old_terrain = self.model.grid_state[row][col]

            self.view.clear_field(row, col)

            self.model.set_terrain(row, col, terrain_type)

            connected_fields = self.model.find_connected_fields(row, col, terrain_type)
            if terrain_type in self.model.connected_terrain_types:
                self.view.draw_terrain(connected_fields, terrain_type)
            else:
                self.view.draw_single_field(row, col, terrain_type)

            if old_terrain and old_terrain in self.model.connected_terrain_types:
                old_connected_fields = self.model.find_connected_fields(row, col, old_terrain)
                old_connected_fields = [f for f in old_connected_fields if f != (row, col)]
                if old_connected_fields:
                    self.view.draw_terrain(old_connected_fields, old_terrain)