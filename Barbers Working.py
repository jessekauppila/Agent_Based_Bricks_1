import mesa
import random

class Barbers(mesa.Agent):
    """An agent with availability or not"""

    def __init__(self, unique_id, model):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)

        # Create the barbers's current_hair_cut_length variable and set the initial values.
        #self.current_hair_cut_length = random.randint(20,40)
        self.current_hair_cut_length = 5

    def step(self):
        # For demonstration purposes I'll print the agent's unique_id
        print(f"Hi, I am barber number {str(self.unique_id)}, I have {str(self.current_hair_cut_length)} minutes left cutting hair.")
        if self.current_hair_cut_length > 0:
            self.current_hair_cut_length -= 1


class BarberShopModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, num_barbers):
        super().__init__()
        self.num_barbers = num_barbers
        # Create scheduler and assign it to the model
        self.schedule = mesa.time.RandomActivation(self)

        # Create agents
        for i in range(self.num_barbers ):
            a = Barbers(i, self)
            # Add the agent to the scheduler
            self.schedule.add(a)

    def step(self):
        """Advance the model by one step."""
        # The model's step will go here for now this will call the step method of each agent and print the agent's unique_id
        self.schedule.step()
        minute = 1
        # customer_number = 1
        # if minute > 5:
        #     new_customer = Customer(customer_number, self)
        #     self.schedule.add(new_customer)
        #     customer_number += 1


model = BarberShopModel(4)
for i in range(20):
    model.step()