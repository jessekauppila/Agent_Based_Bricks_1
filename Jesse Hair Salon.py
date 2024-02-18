import mesa
import random


class Barbers(mesa.Agent):
    """An agent with availability or not"""

    def __init__(self, unique_id, model, customer=None):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)

        # Create the barbers's current_hair_cut_length variable and set the initial values.
        # self.current_hair_cut_length = random.randint(20,40)
        self.current_hair_cut_length = 0

        self.customer_in_chair = customer

    def step(self):
        # Who's hair is the barber cutting:

        # For demonstration purposes I'll print the agent's unique_id
        print(
            f"Hi, Barber {str(self.unique_id)}, hair cut length left: {str(self.current_hair_cut_length)}")
        if self.customer_in_chair is not None:
            print(f"Cutting customer: {str(self.customer_in_chair)}")

        if self.current_hair_cut_length > 0:
            self.current_hair_cut_length -= 1


class Customer(mesa.Agent):

    def __init__(self, unique_id, model):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)
        self.time_waiting = 0
        self.marked_for_removal = False  # Flag to indicate if the customer should be removed
        self.marked_as_waiting = True
        self.marked_as_getting_haircut = False
        self.current_hair_cut_length = 0

    def step(self):
        # For demonstration purposes I'll print the agent's unique_id
        if self.marked_as_waiting:
            print(f"Customer {str(self.unique_id)} waited {str(self.time_waiting)} minutes.")

        if self.marked_as_getting_haircut:
            print(
                f"Customer {str(self.unique_id)} getting cut for {str(self.current_hair_cut_length)} minutes.")

        # tracks the amount of time customer is waiting
        self.time_waiting += 1

        # tracks the amount of time customer to see when they leave.
        if self.time_waiting > 5 and self.marked_as_waiting is True:
            print(f"Customer {str(self.unique_id)} waited {str(self.time_waiting)} minutes, ANGRY, leaves.")
            # self.manager.remove_customer(self)  # Remove the customer from the manager
            self.marked_as_waiting = False
            self.marked_as_getting_haircut = False
            self.marked_for_removal = True  # Mark the customer for removal from the schedule

        if self.current_hair_cut_length == 0 and self.marked_as_getting_haircut == False:
            print(f"Customer {str(self.unique_id)} finished haircut")
            self.marked_as_waiting = False
            self.marked_as_getting_haircut = False
            self.marked_for_removal = True  # Mark the customer for removal from the schedule

    def remove_from_schedule(self):
        if self.marked_for_removal:
            self.model.schedule.remove(self)

    # maybe I really need to change this above! ^^^^
    # to something like
    # if self.


class Time(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.time = 0
        self.customer_number = None

    def step(self):
        if self.time % 3 == 0:
            if self.customer_number is None:
                self.customer_number = 1
            customer = Customer(self.customer_number, self.model)  # Pass manager
            self.customer_number += 1
            self.model.schedule.add(customer)  # Add the customer to the scheduler

        self.time += 1  # Increment time


class BarberShopModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, num_barbers):
        super().__init__()

        # Create scheduler and assign it to the model
        self.schedule = mesa.time.RandomActivation(self)

        # Initialize Time
        time = Time(1, self)
        self.schedule.add(time)

        # Create barbers
        self.num_barbers = num_barbers
        for i in range(self.num_barbers):
            a = Barbers(i, self, None)
            # Add the agent to the scheduler
            self.schedule.add(a)

        # Initialize the longest waiting customer and their waiting time
        self.longest_waiting_customer_num = 1
        self.longest_waiting_time = 0

    def step(self):
        """Advance the model by one step."""
        # The model's step will go here for now this will call the step method of each agent and print the agent's unique_id
        self.schedule.step()

        # Remove customers marked for removal after all agents have stepped
        for agent in self.schedule.agents:
            if isinstance(agent, Customer) and agent.marked_for_removal:
                agent.remove_from_schedule()

        # Find the customer with the longest waiting time
        for agent in self.schedule.agents:
            if isinstance(agent,
                          Customer) and agent.time_waiting > self.longest_waiting_time and agent.marked_as_waiting == True:
                self.longest_waiting_customer_num = agent.unique_id
                self.longest_waiting_time = agent.time_waiting
                print(
                    f"Longest waiting customer {self.longest_waiting_customer_num} with {self.longest_waiting_time} minutes wait.")

        # Assign the longest waiting customer to a barber
        for agent in self.schedule.agents:
            if isinstance(agent, Barbers) and agent.current_hair_cut_length == 0:

                for customer_longest_waiting in self.schedule.agents:
                    if isinstance(customer_longest_waiting,
                                  Customer) and customer_longest_waiting.unique_id == self.longest_waiting_customer_num and customer_longest_waiting.marked_as_waiting:
                        agent.customer_in_chair = self.longest_waiting_customer_num  # Assign the customer instance
                        # to the barber
                        starting_hair_cut_length = 5  # create length of time of haircut

                        agent.current_hair_cut_length = starting_hair_cut_length
                        self.longest_waiting_time = 0  # Reset the longest waiting time

                        customer_longest_waiting.marked_as_waiting = False
                        customer_longest_waiting.marked_as_getting_haircut = True
                        customer_longest_waiting.current_hair_cut_length = starting_hair_cut_length
                        break

        for customer in self.schedule.agents:
            if isinstance(customer, Customer) and customer.current_hair_cut_length > 0 and customer.marked_as_getting_haircut == True:
                customer.current_hair_cut_length -= 1
            elif isinstance(customer,Customer) and customer.current_hair_cut_length == 0 and customer.marked_as_getting_haircut == True:
                customer.remove_from_schedule()
                for barber in self.schedule.agents:
                    if (isinstance(barber, Barbers) and barber.customer_in_chair == customer.unique_id):
                        barber.customer_in_chair = None


##############################################
#### Why does customer 1 never disappear?
#
# Have to end cutting customer 1 ####
##############################################


model = BarberShopModel(1)
for i in range(30):
    model.step()

# get rid of TIME Class
# add time to BarberShopModel
# add time of haircut to Customer Model
# remover customer after they get the correct haircut...
