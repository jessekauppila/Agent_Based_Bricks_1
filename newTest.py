import mesa

class Time(mesa.Agent):
    def __init__(self, unique_id, model):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)

        # Create the agent's attribute and set the initial values.
        self.time = 0
        self.customer_number = 1
        self.manager = CustomerManager()  # Initialize manager as an instance variable.

    def step(self):
        if self.time % 5 == 0:
            customer = Customer(self.customer_number, self, self.manager)  # Pass manager
            self.customer_number += 1
            self.model.schedule.add(customer)  # Access the model's schedule and add the customer

        self.time += 1  # Increment time

class Customer(mesa.Agent):

    def __init__(self, unique_id, model, manager):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)
        self.time_waiting = 0
        self.manager = manager
        self.manager.add_customer(self)  # Add the customer to the manager upon creation

    def step(self):
        # For demonstration purposes I'll print the agent's unique_id
        print(f"Hi, I'm customer {str(self.unique_id)}, I have waited {str(self.time_waiting)} minutes.")

        # tracks the amount of time customer is waiting
        self.time_waiting += 1

        # tracks the amount of time customer to see when they leave.
        if self.time_waiting > 5:
            print(f"Hi, I'm customer {str(self.unique_id)}, I have waited {str(self.time_waiting)} minutes, I'm ANGRY and leave.")
            self.manager.remove_customer(self)  # Remove the customer from the manager
            self.model.schedule.remove(self)  # Remove the customer from the scheduler

class CustomerManager:
    def __init__(self):
        self.customers = []

    def add_customer(self, customer):
        self.customers.append(customer)

    def remove_customer(self, customer):
        if customer in self.customers:
            self.customers.remove(customer)
        else:
            print("Customer not found in the list.")

    def get_all_customers(self):
        return self.customers

class BarberShopModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self):
        super().__init__()
        # Create scheduler and assign it to the model
        self.schedule = mesa.time.RandomActivation(self)

        # Initialize Time
        time = Time(1, self)
        self.schedule.add(time)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()

model = BarberShopModel()
for i in range(30):
    model.step()
