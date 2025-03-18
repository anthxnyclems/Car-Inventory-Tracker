import csv  # Import CSV module to handle file operations

# Define the Car class to store individual car details
class Car:
    def __init__(self, make, model, year, price, status="Available"):
        """
        Initialize a Car object.

        :param make: Car manufacturer (e.g., Toyota, Ford)
        :param model: Specific model of the car (e.g., Camry, Mustang)
        :param year: Manufacturing year of the car (integer)
        :param price: Price of the car (float)
        :param status: Availability status (default: "Available", can be "Sold")
        """
        self.make = make
        self.model = model
        self.year = int(year)  # Convert year to an integer
        self.price = float(price)  # Convert price to a float
        self.status = status  # Default is "Available"

# Define the Inventory class to manage the list of cars
class Inventory:
    def __init__(self, filename='inventory.csv'):
        """
        Initialize an Inventory object that loads cars from a CSV file.

        :param filename: Name of the CSV file to store inventory (default: 'inventory.csv')
        """
        self.filename = filename
        self.cars = []  # List to store Car objects
        self.load_inventory()  # Load cars from file on initialization

    def load_inventory(self):
        """
        Load inventory data from a CSV file. If the file does not exist, create an empty file.
        """
        try:
            with open(self.filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header row

                # Convert each row into a Car object and add it to the list
                self.cars = [Car(*row) for row in reader]

        except FileNotFoundError:
            # If the file is missing, create an empty inventory file
            with open(self.filename, mode='w', newline='') as file:
                pass  # Just create an empty file, no cars added

    def save_inventory(self):
        """
        Save the current inventory list to the CSV file.
        """
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(["Make", "Model", "Year", "Price", "Status"])

            # Write each car's details into the CSV file
            for car in self.cars:
                writer.writerow([car.make, car.model, car.year, car.price, car.status])

    def add_car(self, make, model, year, price):
        """
        Add a new car to the inventory.

        :param make: Car manufacturer
        :param model: Car model
        :param year: Manufacturing year
        :param price: Price of the car
        """
        self.cars.append(Car(make, model, year, price))  # Add new car object
        self.save_inventory()  # Save updated inventory to file

    def remove_car(self, model):
        """
        Remove a car from the inventory based on its model.

        :param model: The model of the car to remove
        """
        self.cars = [car for car in self.cars if car.model.lower() != model.lower()]
        self.save_inventory()  # Save updated inventory to file

    def toggle_sold_status(self, model):
        """
        Toggles the status of a car between 'Sold' and 'Available'.
        """
        for car in self.cars:
            if car.model.lower() == model.lower():
                car.status = "Available" if car.status == "Sold" else "Sold"
        self.save_inventory()


    def search_cars(self, make=None, min_price=None, max_price=None, min_year=None):
        """
        Search for cars that match specific criteria.

        :param make: (Optional) Filter by car manufacturer
        :param min_price: (Optional) Filter by minimum price
        :param max_price: (Optional) Filter by maximum price
        :param min_year: (Optional) Filter by minimum manufacturing year

        :return: List of cars matching the search criteria
        """
        results = [
            car for car in self.cars if
            (make is None or car.make.lower() == make.lower()) and
            (min_price is None or car.price >= float(min_price)) and
            (max_price is None or car.price <= float(max_price)) and
            (min_year is None or car.year >= int(min_year))
        ]
        return results  # Return filtered list of cars
