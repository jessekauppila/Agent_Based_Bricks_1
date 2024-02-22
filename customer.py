from mesa import Agent
from barber import Barber

class Customer(Agent):
    def __init__(self, unique_id, model, barbershop_model):
        super().__init__(unique_id, model)
        self.time_waiting = 0
        self.marked_as_waiting = True
        self.marked_as_getting_haircut = False
        self.marked_as_finished_haircut = False
        self.marked_as_left_angry = False
        self.current_hair_cut_length = 0
        self.my_barber = None
        self.barbershop_model = barbershop_model

    def step(self):
        self.mark_as_waiting()
        self.customer_leaves()
        self.finishing_haircut()  # Pass the model argument here
        self.time_waiting += 1

    def mark_as_waiting(self):
        if self.marked_as_getting_haircut:
            self.marked_as_waiting = False

    def customer_leaves(self):
        if self.time_waiting > 10 and self.marked_as_waiting == True and self.marked_as_left_angry == False:
            model = self.model  # Access the model object
            print(f"[{model.convert_to_hh_mm(model.clock_time)}] Customer {self.unique_id} leaves frustrated.")
            self.marked_as_left_angry = True
            self.marked_as_waiting = False
            self.time_waiting = 0
            self.remove()
            self.barbershop_model.find_longest_waiting_customer()

    def finishing_haircut(self):
        if self.current_hair_cut_length == 0 and self.marked_as_getting_haircut:
            self.marked_as_finished_haircut = True
            self.remove()
            model = self.model  # Access the model object
            print(f"[{model.convert_to_hh_mm(model.clock_time)}] Barber {self.my_barber} finished cutting customer {self.unique_id}")
            print(f"[{model.convert_to_hh_mm(model.clock_time)}] Customer {self.unique_id} leaves satisfied")
            for agent in model.schedule.agents:
                if isinstance(agent, Barber) and agent.my_customer == self.unique_id:
                    agent.my_customer = None
        else:
            self.current_hair_cut_length -= 1
