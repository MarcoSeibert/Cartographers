import tkinter as tk
from tkinter import ttk

# Terrain types and their symbols (for display)
TERRAIN_TYPES = {
    "Leer": "",
    "Wald": "🌳",
    "Dorf": "🏡",
    "Wasser": "💧",
    "Berg": "⛰️",
    "Farm": "🌾",
    "Ruine": "🏛️",
    "Monster": "👹",
    "Straße": "🛣️"
}


class CartographersGUI:
    def __init__(self, root, size=11):
        self.root = root
        self.size = size
        self.grid = [["Leer" for _ in range(size)] for _ in range(size)]
        self.buttons = {}

        self.setup_ui()

    def setup_ui(self):
        # Create the main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        # Create the grid
        for row in range(self.size):
            for col in range(self.size):
                button = tk.Button(
                    main_frame,
                    text="",
                    width=4,
                    height=2,
                    command=lambda r=row, c=col: self.on_cell_click(r, c)
                )
                button.grid(row=row, column=col, padx=1, pady=1)
                self.buttons[(row, col)] = button

        # Add a label for instructions
        tk.Label(
            self.root,
            text="Klicke auf ein Feld, um den Geländetyp auszuwählen."
        ).pack(pady=5)

    def on_cell_click(self, row, col):
        # Create a dropdown menu for terrain selection
        menu = tk.Menu(self.root, tearoff=0)
        for terrain in TERRAIN_TYPES:
            menu.add_command(
                label=terrain,
                command=lambda t=terrain: self.set_terrain(row, col, t)
            )
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())

    def set_terrain(self, row, col, terrain):
        self.grid[row][col] = terrain
        symbol = TERRAIN_TYPES[terrain]
        self.buttons[(row, col)].config(text=symbol)

    def update_dynamic_terrain(self, row, col):
        # Placeholder for dynamic terrain logic
        # Example: If a village is next to water, turn it into a dock
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Der Kartograph - Sandbox")
    app = CartographersGUI(root)
    root.mainloop()