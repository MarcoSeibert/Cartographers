import tkinter as tk


# --- MODEL ---
class BoardModel:
    def __init__(self, size=11):
        self.size = size
        self.boardstate = [["Leer" for _ in range(size)] for _ in range(size)]
        self.dynamic_boardstate = [["Leer" for _ in range(size)] for _ in range(size)]

        # Terrain types and their abbreviations
        self.terrain_types = {
            "Leer": "",
            "Wald": "WA",
            "Dorf": "DO",
            "Acker": "AC",
            "Wasser": "WS",
            "Monster": "MO",
            "Gebirge": "GE",
            "Ruine": "RU",
            "Held": "HE"
        }

    def set_terrain(self, row, col, terrain):
        if 0 <= row < self.size and 0 <= col < self.size:
            self.boardstate[row][col] = terrain
            self.dynamic_boardstate[row][col] = terrain

    def get_boardstate(self):
        return self.boardstate

    def get_dynamic_boardstate(self):
        return self.dynamic_boardstate

    def get_terrain_abbreviation(self, terrain):
        return self.terrain_types.get(terrain, "")


# --- VIEW ---
class BoardView:
    def __init__(self, _root, model, controller):
        self.root = _root
        self.model = model
        self.controller = controller
        self.size = model.size

        self.input_buttons = {}
        self.display_labels = {}

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        # Input table (left)
        input_frame = tk.LabelFrame(main_frame, text="Eingabe", padx=5, pady=5)
        input_frame.grid(row=0, column=0, padx=10)

        # Display table (right)
        display_frame = tk.LabelFrame(main_frame, text="Anzeige", padx=5, pady=5)
        display_frame.grid(row=0, column=1, padx=10)

        # Initialize input table
        for row in range(self.size):
            for col in range(self.size):
                button = tk.Button(
                    input_frame,
                    text="",
                    width=4,
                    height=2,
                    command=lambda r=row, c=col: self.controller.on_cell_click(r, c)
                )
                button.grid(row=row, column=col, padx=1, pady=1)
                self.input_buttons[(row, col)] = button

        # Initialize display table
        for row in range(self.size):
            for col in range(self.size):
                cell_frame = tk.Frame(display_frame, bd=1, relief=tk.SUNKEN)
                cell_frame.grid(row=row, column=col, padx=1, pady=1)

                base_label = tk.Label(cell_frame, text="", width=4, height=1)
                base_label.pack()

                dynamic_label = tk.Label(cell_frame, text="", width=4, height=1)
                dynamic_label.pack()

                self.display_labels[(row, col)] = (base_label, dynamic_label)

        # Instructions
        tk.Label(
            self.root,
            text="Klicke auf ein Feld in der Eingabe-Tabelle, um den Geländetyp auszuwählen."
        ).pack(pady=5)

    def update_cell(self, row, col):
        terrain = self.model.boardstate[row][col]
        abbreviation = self.model.get_terrain_abbreviation(terrain)

        # Update input table
        self.input_buttons[(row, col)].config(text=abbreviation)

        # Update display table
        base_label, dynamic_label = self.display_labels[(row, col)]
        base_label.config(text=abbreviation)
        dynamic_label.config(text=abbreviation)


# --- CONTROLLER ---
class BoardController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def on_cell_click(self, row, col):
        # Create a dropdown menu for terrain selection
        menu = tk.Menu(self.view.root, tearoff=0)
        for terrain in self.model.terrain_types:
            menu.add_command(
                label=terrain,
                command=lambda t=terrain: self.set_terrain(row, col, t)
            )
        menu.post(self.view.root.winfo_pointerx(), self.view.root.winfo_pointery())

    def set_terrain(self, row, col, terrain):
        self.model.set_terrain(row, col, terrain)
        self.view.update_cell(row, col)


# --- MAIN APPLICATION ---
class CartographersApp:
    def __init__(self, _root):
        self.model = BoardModel()
        self.controller = BoardController(self.model, None)  # Temporary None for view
        self.view = BoardView(_root, self.model, self.controller)
        self.controller.view = self.view  # Assign view after initialization

    def get_boardstate(self):
        return self.model.get_boardstate()

    def get_dynamic_boardstate(self):
        return self.model.get_dynamic_boardstate()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Der Kartograph - MVC Sandbox")
    app = CartographersApp(root)
    root.mainloop()