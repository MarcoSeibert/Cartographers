import tkinter as tk

# Terrain types and their abbreviations
TERRAIN_TYPES = {
    "Leer": "",
    "Wald": "WA",
    "Dorf": "DO",
    "Wasser": "WS",
    "Berg": "BE",
    "Farm": "FA",
    "Ruine": "RU",
    "Monster": "MO"
}



class CartographersGUI:
    def __init__(self, _root, size=11):
        self.root = _root
        self.size = size
        self.grid = [["Leer" for _ in range(size)] for _ in range(size)]
        self.dynamic_grid = [["Leer" for _ in range(size)] for _ in range(size)]
        self.buttons = {}
        self.labels = {}

        self.setup_ui()

    def setup_ui(self):
        # Create the main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        # Create the grid
        for row in range(self.size):
            for col in range(self.size):
                # Frame to hold both the button and the label
                cell_frame = tk.Frame(main_frame, bd=1, relief=tk.RAISED)
                cell_frame.grid(row=row, column=col, padx=1, pady=1)

                # Button for terrain selection
                button = tk.Button(
                    cell_frame,
                    text="",
                    width=4,
                    height=1,
                    command=lambda r=row, c=col: self.on_cell_click(r, c)
                )
                button.pack()
                self.buttons[(row, col)] = button

                # Label for dynamic terrain type
                label = tk.Label(cell_frame, text="", width=4, height=1)
                label.pack()
                self.labels[(row, col)] = label

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
        abbreviation = TERRAIN_TYPES[terrain]
        self.buttons[(row, col)].config(text=abbreviation)

        # Set dynamic terrain label to match the base terrain for now
        self.dynamic_grid[row][col] = terrain
        self.labels[(row, col)].config(text=abbreviation)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Der Kartograph - Sandbox")
    app = CartographersGUI(root)
    root.mainloop()