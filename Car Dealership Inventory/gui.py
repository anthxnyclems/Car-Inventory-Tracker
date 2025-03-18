import tkinter as tk
from tkinter import ttk, messagebox
from inventory import Inventory  # Import Inventory class to manage car data

class InventoryApp:
    def __init__(self, root):
        """
        Initialize the InventoryApp with a Tkinter root window.
        """
        self.inventory = Inventory()  # Create an instance of Inventory to manage cars
        self.root = root
        self.root.title("Car Dealership Inventory")  # Set window title
        self.selected_cars = set()  # Track selected cars for bulk actions

        # Configure the root window for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.create_widgets()  # Initialize the UI components

    def create_widgets(self):
        """
        Create and arrange all UI components.
        """
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")

        # Allow the frame to expand with the window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        for i in range(8):  # Set equal width for all columns
            frame.columnconfigure(i, weight=1)

        # Labels and Input Fields for Adding/Searching Cars
        ttk.Label(frame, text="Make:").grid(row=0, column=0)
        self.make_entry = ttk.Entry(frame)
        self.make_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame, text="Model:").grid(row=0, column=2)
        self.model_entry = ttk.Entry(frame)
        self.model_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(frame, text="Year:").grid(row=0, column=4)
        self.year_entry = ttk.Entry(frame)
        self.year_entry.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        ttk.Label(frame, text="Price:").grid(row=0, column=6)
        self.price_entry = ttk.Entry(frame)
        self.price_entry.grid(row=0, column=7, padx=5, pady=5, sticky="ew")

        # Buttons for Actions (Add, Remove, Mark as Sold, Search)
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, columnspan=8, pady=5)

        ttk.Button(button_frame, text="Add Car", command=self.add_car).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Remove Car", command=self.remove_car).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Mark/Unmark as Sold", command=self.mark_as_sold).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Search", command=self.search_cars).grid(row=0, column=3, padx=5)

        # Treeview (Inventory List) with Scrollbars
        tree_frame = ttk.Frame(frame)
        tree_frame.grid(row=2, column=0, columnspan=8, sticky="nsew")

        frame.rowconfigure(2, weight=1)  # Allow table to expand with window

        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")  # Vertical scrollbar
        self.tree = ttk.Treeview(tree_frame, columns=("Select", "Make", "Model", "Year", "Price", "Status"), show="headings", yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.tree.yview)

        # Table Headers
        self.tree.heading("Select", text="✔", anchor=tk.W)  # Checkbox column
        self.tree.heading("Make", text="Make")
        self.tree.heading("Model", text="Model")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Status", text="Status")

        # Column Sizes
        self.tree.column("Select", width=50, anchor=tk.W)
        self.tree.column("Make", width=150)
        self.tree.column("Model", width=150)
        self.tree.column("Year", width=100)
        self.tree.column("Price", width=150)
        self.tree.column("Status", width=150)

        self.tree.pack(side="left", fill="both", expand=True)  # Expand the table to fit
        tree_scroll.pack(side="right", fill="y")  # Attach scrollbar

        # Event binding for selection toggle (checkbox simulation)
        self.tree.bind("<ButtonRelease-1>", self.toggle_selection)

        # Load inventory data into the table
        self.load_inventory_into_tree()

    def toggle_selection(self, event):
        """
        Handles toggling checkboxes for selecting cars.
        """
        item = self.tree.identify_row(event.y)
        if item:
            model = self.tree.item(item, "values")[2]  # Get car model from the row
            if model in self.selected_cars:
                self.selected_cars.remove(model)
                self.tree.item(item, values=("☐", *self.tree.item(item, "values")[1:]))
            else:
                self.selected_cars.add(model)
                self.tree.item(item, values=("✔", *self.tree.item(item, "values")[1:]))


    def add_car(self):
        """
        Adds a new car to the inventory based on user input.
        """
        make = self.make_entry.get()
        model = self.model_entry.get()
        year = self.year_entry.get()
        price = self.price_entry.get()
        if make and model and year and price:
            self.inventory.add_car(make, model, year, price)
            self.load_inventory_into_tree()
            messagebox.showinfo("Success", "Car added successfully!")
        else:
            messagebox.showerror("Error", "All fields are required")


    def remove_car(self):
        """
        Removes selected cars from the inventory.
        """
        if not self.selected_cars:
            messagebox.showerror("Error", "Select at least one car to remove")
            return
        
        for model in self.selected_cars:
            self.inventory.remove_car(model)
        
        self.selected_cars.clear()
        self.load_inventory_into_tree()
        messagebox.showinfo("Success", "Car(s) removed successfully!")


    def mark_as_sold(self):
        """
        Toggles the selected cars between 'Sold' and 'Available'.
        """
        if not self.selected_cars:
            messagebox.showerror("Error", "Select at least one car to toggle sale status")
            return

        for model in self.selected_cars:
            self.inventory.toggle_sold_status(model)

        self.selected_cars.clear()
        self.load_inventory_into_tree()
        messagebox.showinfo("Success", "Car sale status updated!")



    def search_cars(self):
        """
        Searches for cars based on user input filters.
        """
        make = self.make_entry.get()
        min_price = self.price_entry.get()
        min_year = self.year_entry.get()
        results = self.inventory.search_cars(make if make else None,
                                             float(min_price) if min_price else None,
                                             None,  
                                             int(min_year) if min_year else None)
        
        if not results:
            messagebox.showerror("Error", "No cars found with the given criteria")
        
        self.load_inventory_into_tree(results)


    def load_inventory_into_tree(self, cars=None):
        """
        Loads the inventory into the table (Treeview).
        """
        self.tree.delete(*self.tree.get_children())  # Clear existing rows
        self.selected_cars.clear()  # Clear selections

        for car in cars if cars else self.inventory.cars:
            self.tree.insert("", tk.END, values=("☐", car.make, car.model, car.year, car.price, car.status))
