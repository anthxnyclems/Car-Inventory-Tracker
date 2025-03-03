import tkinter as tk
from tkinter import ttk, messagebox
import csv

# Define a Car class to represent each car entry
class Car:
    def __init__(self, make, model, year, price, status="Available"):
        self.make = make
        self.model = model
        self.year = int(year)
        self.price = float(price)
        self.status = status

# Inventory class to handle inventory management
class Inventory:
    def __init__(self, filename='inventory.csv'):
        self.filename = filename
        self.cars = []
        self.load_inventory()

    # Load inventory from CSV file
    def load_inventory(self):
        try:
            with open(self.filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip the header row
                self.cars = [Car(*row) for row in reader]
        except FileNotFoundError:
            with open(self.filename, mode='w', newline='') as file:
                pass  # Create empty file if not found

    # Save inventory back to CSV file
    def save_inventory(self):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Make", "Model", "Year", "Price", "Status"])
            for car in self.cars:
                writer.writerow([car.make, car.model, car.year, car.price, car.status])

    # Add a new car to the inventory
    def add_car(self, make, model, year, price):
        self.cars.append(Car(make, model, year, price))
        self.save_inventory()

    # Remove a car from inventory based on the model name
    def remove_car(self, model):
        self.cars = [car for car in self.cars if car.model.lower() != model.lower()]
        self.save_inventory()

    # Mark a car as sold
    def mark_as_sold(self, model):
        for car in self.cars:
            if car.model.lower() == model.lower():
                car.status = "Sold"
        self.save_inventory()

    # Search for cars based on criteria
    def search_cars(self, make=None, min_price=None, max_price=None, min_year=None):
        results = [
            car for car in self.cars if
            (make is None or car.make.lower() == make.lower()) and
            (min_price is None or car.price >= float(min_price)) and
            (max_price is None or car.price <= float(max_price)) and
            (min_year is None or car.year >= int(min_year))
        ]
        return results

# Main application class for the GUI
class InventoryApp:
    def __init__(self, root):
        self.inventory = Inventory()
        self.root = root
        self.root.title("Car Dealership Inventory")
        
        self.create_widgets()

    # Create UI components
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Labels and input fields
        ttk.Label(frame, text="Make:").grid(row=0, column=0)
        self.make_entry = ttk.Entry(frame)
        self.make_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Model:").grid(row=0, column=2)
        self.model_entry = ttk.Entry(frame)
        self.model_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame, text="Year:").grid(row=0, column=4)
        self.year_entry = ttk.Entry(frame)
        self.year_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(frame, text="Price:").grid(row=0, column=6)
        self.price_entry = ttk.Entry(frame)
        self.price_entry.grid(row=0, column=7, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, columnspan=8, pady=5)
        
        ttk.Button(button_frame, text="Add Car", command=self.add_car).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Remove Car", command=self.remove_car).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Mark as Sold", command=self.mark_as_sold).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Search", command=self.search_cars).grid(row=0, column=3, padx=5)

        # Table to display inventory
        self.tree = ttk.Treeview(frame, columns=("Make", "Model", "Year", "Price", "Status"), show='headings')
        self.tree.heading("Make", text="Make")
        self.tree.heading("Model", text="Model")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Status", text="Status")
        self.tree.grid(row=2, column=0, columnspan=8, pady=10)
        
        self.load_inventory_into_tree()

    # Add a car to inventory
    def add_car(self):
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

    # Remove selected car from inventory
    def remove_car(self):
        selected_item = self.tree.selection()
        if selected_item:
            model = self.tree.item(selected_item, "values")[1]
            self.inventory.remove_car(model)
            self.load_inventory_into_tree()
            messagebox.showinfo("Success", "Car removed successfully!")
        else:
            messagebox.showerror("Error", "Select a car to remove")

    # Mark selected car as sold
    def mark_as_sold(self):
        selected_item = self.tree.selection()
        if selected_item:
            model = self.tree.item(selected_item, "values")[1]
            self.inventory.mark_as_sold(model)
            self.load_inventory_into_tree()
            messagebox.showinfo("Success", "Car marked as sold!")
        else:
            messagebox.showerror("Error", "Select a car to mark as sold")

    # Search for cars based on filters
    def search_cars(self):
        make = self.make_entry.get()
        min_price = self.price_entry.get()
        min_year = self.year_entry.get()
        results = self.inventory.search_cars(make if make else None,
                                             float(min_price) if min_price else None,
                                             None,  # No max_price input field
                                             int(min_year) if min_year else None)
        
        if not results:
            messagebox.showerror("Error", "No cars found with the given criteria")
        
        self.load_inventory_into_tree(results)

    # Load inventory data into table
    def load_inventory_into_tree(self, cars=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for car in cars if cars else self.inventory.cars:
            self.tree.insert("", tk.END, values=(car.make, car.model, car.year, car.price, car.status))

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
