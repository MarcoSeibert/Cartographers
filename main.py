import tkinter as tk
from model import BoardModel
from view import BoardView
from controller import BoardController

class CartographersApp:
    def __init__(self, root):
        self.model = BoardModel()
        self.controller = BoardController(self.model, None)
        self.view = BoardView(root, self.model, self.controller)
        self.controller.view = self.view

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Der Kartograph - MVC")
    app = CartographersApp(root)
    root.mainloop()