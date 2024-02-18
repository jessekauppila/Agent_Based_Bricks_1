import mesa

class Time(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.time = 0
        self.customer_number = 1

    def step(self):
        if self.time % 5 == 0:
            customer = Customer(self.customer_number, self.model)  # Pass manager
            self.customer_number += 1
            self.model.schedule.add(customer)  # Add the customer to the scheduler

        self.time += 1  # Increment time


class Customer(mesa.Agent):

    def __init__(self, unique_id, model):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)
        self.time_waiting = 0
        self.marked_for_removal = False  # Flag to indicate if the customer should be removed


    def step(self):
        # For demonstration purposes I'll print the agent's unique_id
        print(f"Hi, I'm customer {str(self.unique_id)}, I have waited {str(self.time_waiting)} minutes.")

        # tracks the amount of time customer is waiting
        self.time_waiting += 1

        # tracks the amount of time customer to see when they leave.
        if self.time_waiting > 5:
            print(f"Hi, I'm customer {str(self.unique_id)}, I have waited {str(self.time_waiting)} minutes, I'm ANGRY and leave.")
            #self.manager.remove_customer(self)  # Remove the customer from the manager
            self.marked_for_removal = True  # Mark the customer for removal from the schedule

    def remove_from_schedule(self):
        if self.marked_for_removal:
            self.model.schedule.remove(self)

class BarberShopModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self):
        super().__init__()
        # Create scheduler and assign it to the model
        self.schedule = mesa.time.RandomActivation(self)

        # Initialize Time
        time = Time(1,self)
        self.schedule.add(time)


    def step(self):
        """Advance the model by one step."""
        self.schedule.step()

        # Remove customers marked for removal after all agents have stepped
        for agent in self.schedule.agents:
            if isinstance(agent, Customer) and agent.marked_for_removal == True:
                agent.remove_from_schedule()

model = BarberShopModel()
for i in range(30):
    model.step()
