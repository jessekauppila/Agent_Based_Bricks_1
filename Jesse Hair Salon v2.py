import mesa
import random

class Haircut:
    """Interface for objects that can be subjected to haircutting."""
    def __init__(self):
        self.current_hair_cut_length = 0

    def receive_haircut(self, length):
        self.current_hair_cut_length = length

    def reduce_haircut_time(self):
        if self.current_hair_cut_length > 0:
            self.current_hair_cut_length -= 1

class Barber(mesa.Agent, Haircut):
    """An agent representing a barber."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.my_customer = None

    def step(self):
        print(f"Barber {str(self.unique_id)}, hair cut left: {str(self.current_hair_cut_length)}")
        if self.my_customer is not None:
            print(f"Cutting customer: {str(self.my_customer.unique_id)}")

        if self.current_hair_cut_length > 0:
            self.reduce_haircut_time()

class Customer(mesa.Agent, Haircut):
    """An agent representing a customer."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.time_waiting = 0
        self.marked_as_waiting = True
        self.marked_as_getting_haircut = False
        self.my_barber = None

    def step(self):
        if self.marked_as_getting_haircut:
            self.marked_as_waiting = False
            print(f"Customer {str(self.unique_id)} getting cut for {str(self.current_hair_cut_length)} minutes with Barber {str(self.my_barber)}.")

        if self.marked_as_waiting is True:
            print(f"Customer {str(self.unique_id)} waited {str(self.time_waiting)} minutes.")
            if self.time_waiting > 5:
                print(f"Customer {str(self.unique_id)} ANGRY, leaves and removed.")
                self.marked_as_waiting = False
                self.remove()

        if self.current_hair_cut_length == 0 and self.marked_as_getting_haircut == True:
            self.remove()
            print(f"Customer {str(self.unique_id)} FINISHED with Barber {str(self.my_barber)} and removed")
            self.my_barber.my_customer = None
            print(f"Barber {str(self.my_barber)} assigned no customers")

        else:
            self.reduce_haircut_time()

        self.time_waiting += 1

class BarbershopModel(mesa.Model):
    """A model representing a barbershop."""
    def __init__(self, num_barbers):
        super().__init__()
        self.schedule = mesa.time.RandomActivation(self)
        self.num_barbers = num_barbers
        self.longest_waiting_customer = None
        self.longest_waiting_time = 0
        self.time = 0
        self.num_in_waiting_room = 0  # Initialize the waiting room size counter
        self.customer_count = 0



    def step(self):
        #self.schedule_agents()  # Schedule new customers
        self.execute_barber_actions()  # Execute barber actions
        self.waiting_room()  # Print waiting room size
        self.create_customer()
        self.time += 1  # Increment time

    def create_customer(self):
        if self.time % 3 == 0:
            customer = Customer(self.customer_count, self)  # Create a new customer with a unique ID
            self.customer_count += 1  # Increment the customer count for the next customer
            self.schedule.add(customer)  # Add the customer to the scheduler

    def execute_barber_actions(self):
        for agent in self.schedule.agents:
            if isinstance(agent, Customer) and agent.time_waiting > self.longest_waiting_time and agent.marked_as_waiting:
                self.longest_waiting_customer = agent
                self.longest_waiting_time = agent.time_waiting
                print(f"Longest waiting customer {self.longest_waiting_customer.unique_id} with {self.longest_waiting_time} minutes wait.")

        for agent in self.schedule.agents:
            if isinstance(agent, Barber) and agent.my_customer is None and self.longest_waiting_customer:
                agent.my_customer = self.longest_waiting_customer
                starting_hair_cut_length = 5
                agent.receive_haircut(starting_hair_cut_length)
                self.longest_waiting_time = 0
                self.longest_waiting_customer.marked_as_waiting = False
                self.longest_waiting_customer.marked_as_getting_haircut = True
                self.longest_waiting_customer.receive_haircut(starting_hair_cut_length)
                self.longest_waiting_customer.my_barber = agent

    def waiting_room(self):
        self.num_in_waiting_room = sum(1 for agent in self.schedule.agents if isinstance(agent, Customer) and agent.marked_as_waiting)
        print(f"Waiting room size: {self.num_in_waiting_room}.")


model = BarbershopModel(1)
#model.schedule.add(time_agent)
for i in range(30):
    model.step()
