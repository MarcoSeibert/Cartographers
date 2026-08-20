import tkinter as tk
from PIL import Image, ImageTk
import random

class BoardView:
    def __init__(self, root, model, controller):
        self.root = root
        self.model = model
        self.controller = controller
        self.cell_size = 50
        self.canvas_width = model.grid_size * self.cell_size
        self.canvas_height = model.grid_size * self.cell_size

        self.canvas = tk.Canvas(
            root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="white"
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", controller.on_canvas_click)

        self.terrain_pinsel = {
            "WA": ["pinsel/baum1.png", "pinsel/baum2.png"],
            "AC": ["pinsel/acker1.png", "pinsel/acker2.png"],
            "WS": ["pinsel/wasser1.png", "pinsel/wasser2.png"],
            "DO": ["pinsel/haus1.png", "pinsel/haus2.png"],
            "MO": ["pinsel/monster1.png", "pinsel/monster2.png"],
        }

        self.pinsel_images = {}
        for terrain_type, pinsel_list in self.terrain_pinsel.items():
            self.pinsel_images[terrain_type] = []
            for pinsel_path in pinsel_list:
                try:
                    image = Image.open(pinsel_path)
                    image = image.resize((15, 15))
                    photo = ImageTk.PhotoImage(image)
                    self.pinsel_images[terrain_type].append(photo)
                except Exception as e:
                    print(f"Fehler beim Laden von {pinsel_path}: {e}")

        self.current_terrain = tk.StringVar(value="WA")
        terrain_dropdown = tk.OptionMenu(
            root,
            self.current_terrain,
            *model.terrain_types,
            command=controller.on_terrain_selected
        )
        terrain_dropdown.pack()

        self.draw_grid()

    def draw_grid(self):
        for i in range(self.model.grid_size + 1):
            self.canvas.create_line(
                i * self.cell_size, 0,
                i * self.cell_size, self.canvas_height,
                fill="lightgray"
            )
            self.canvas.create_line(
                0, i * self.cell_size,
                self.canvas_width, i * self.cell_size,
                fill="lightgray"
            )

    def clear_field(self, row, col):
        for terrain_type in self.terrain_pinsel.keys():
            self.canvas.delete(f"{terrain_type}_{row}_{col}")

    def draw_terrain(self, connected_fields, terrain_type):
        # Lösche alle Pinsel in den verbundenen Feldern
        for row, col in connected_fields:
            self.canvas.delete(f"{terrain_type}_{row}_{col}")

        if not connected_fields:
            return

        # Anzahl der Pinsel proportional zur Anzahl der Felder (8 pro Feld)
        pinsel_count = len(connected_fields) * 8

        # Verteile Pinsel über die verbundenen Felder
        all_pinsels = []
        for _ in range(pinsel_count):
            pinsel = random.choice(self.pinsel_images[terrain_type])
            # Wähle zufällig ein Feld aus den verbundenen Feldern
            row, col = random.choice(list(connected_fields))
            # Platziere den Pinsel zufällig im Feld (inkl. 7 Pixel Überlappung)
            x = col * self.cell_size + random.randint(-7, self.cell_size + 7 - 15)
            y = row * self.cell_size + random.randint(-7, self.cell_size + 7 - 15)
            # Prüfe, ob der Pinsel innerhalb der Canvas liegt
            if 0 <= x < self.canvas_width - 15 and 0 <= y < self.canvas_height - 15:
                # Bestimme alle Felder, die der Pinsel berührt
                row_start = y // self.cell_size
                row_end = (y + 14) // self.cell_size
                col_start = x // self.cell_size
                col_end = (x + 14) // self.cell_size

                touched_fields = []
                for r in range(row_start, row_end + 1):
                    for c in range(col_start, col_end + 1):
                        if 0 <= r < self.model.grid_size and 0 <= c < self.model.grid_size:
                            touched_fields.append((r, c))

                all_pinsels.append((pinsel, x, y, touched_fields))

        # Sortiere nach y-Koordinate (Hintergrund → Vordergrund)
        all_pinsels.sort(key=lambda item: item[2])

        # Zeichne alle Pinsel
        for pinsel, x, y, touched_fields in all_pinsels:
            tags = [f"{terrain_type}_{r}_{c}" for r, c in touched_fields]
            self.canvas.create_image(
                x, y,
                anchor="nw",
                image=pinsel,
                tags=" ".join(tags)
            )

    def draw_single_field(self, row, col, terrain_type):
        self.canvas.delete(f"{terrain_type}_{row}_{col}")

        pinsel = random.choice(self.pinsel_images[terrain_type])
        x = col * self.cell_size + (self.cell_size - 15) // 2
        y = row * self.cell_size + (self.cell_size - 15) // 2

        row_start = y // self.cell_size
        row_end = (y + 14) // self.cell_size
        col_start = x // self.cell_size
        col_end = (x + 14) // self.cell_size

        touched_fields = []
        for r in range(row_start, row_end + 1):
            for c in range(col_start, col_end + 1):
                if 0 <= r < self.model.grid_size and 0 <= c < self.model.grid_size:
                    touched_fields.append((r, c))

        tags = [f"{terrain_type}_{r}_{c}" for r, c in touched_fields]
        self.canvas.create_image(
            x, y,
            anchor="nw",
            image=pinsel,
            tags=" ".join(tags)
        )