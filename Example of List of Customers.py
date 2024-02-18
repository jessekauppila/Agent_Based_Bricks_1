import mesa

class Customer(mesa.Agent):
    """An agent with availability or not"""

    def __init__(self, unique_id, model, manager):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)
        self.time_waiting = 0
        self.manager = manager
        self.manager.add_customer(self)  # Add the customer to the manager upon creation

    def step(self):
        # For demonstration purposes I'll print the agent's unique_id
        print(f"Hi, I'm customer {str(self.unique_id)}, I have waited {str(self.time_waiting)} minutes.")
        if self.time_waiting > 20:
            print(f"Hi, I'm customer number {str(self.unique_id)} is ANGRY and leaves.")
            self.manager.remove_customer(self)  # Remove the customer from the manager
            self.remove()
        self.time_waiting += 1


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


# Example usage:
manager = CustomerManager()

# Creating customers and adding them to the manager
customer1 = Customer(1, None, manager)
customer2 = Customer(2, None, manager)
customer3 = Customer(3, None, manager)

# Accessing all customers
all_customers = manager.get_all_customers()

# Iterating through all customers
for customer in all_customers:
    print(f"Customer ID: {customer.unique_id}, Time Waiting: {customer.time_waiting} minutes")
