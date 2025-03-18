import tkinter as tk
from gui import InventoryApp

if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')  # Start maximized
    root.minsize(900, 600)  # Prevent from getting too small
    app = InventoryApp(root)
    root.mainloop()
