from mesa import Agent


class Barber(Agent):
    """An agent with availability or not"""

    def __init__(self, unique_id, model, customer=None, time_on_shift=0):
        super().__init__(unique_id, model)
        self.current_hair_cut_length = 0
        self.my_customer = customer
        self.time_on_shift = time_on_shift
        self.on_shift = True

    def step(self):
        # Who's hair is the barber cutting:
        # if self.my_customer is not None:
            # print(
            #     f"Barber {str(self.unique_id)}, hair cut left: {str(self.current_hair_cut_length)}")
            # print(f" Cutting customer: {str(self.my_customer)}")
        # else:
        #     print (f"Barber {str(self.unique_id)} available!")

        if self.current_hair_cut_length > 0:
            self.current_hair_cut_length -= 1