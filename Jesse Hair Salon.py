import mesa
import random


class Barber(mesa.Agent):
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


class Customer(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.time_waiting = 0
        self.marked_as_waiting = True
        self.marked_as_getting_haircut = False
        self.marked_as_finished_haircut = False
        self.marked_as_left_angry = False
        self.current_hair_cut_length = 0
        self.my_barber = None

    def step(self):
        self.mark_as_waiting()
        self.customer_leaves()
        self.finishing_haircut()
        self.time_waiting += 1

    def mark_as_waiting(self):
        if self.marked_as_getting_haircut:
            self.marked_as_waiting = False
            # print(
                # f"Customer {str(self.unique_id)} getting cut for {str(self.current_hair_cut_length)} minutes with Barber {str(self.my_barber)}.")

    def customer_leaves(self):
        # if self.marked_as_waiting is True:
            #print(f"Customer {str(self.unique_id)} waited {str(self.time_waiting)} minutes.")
        if self.time_waiting > 5 and self.marked_as_waiting is True:
            print(f"Customer {str(self.unique_id)} ANGRY, leaves and removed.")
            self.marked_as_left_angry = True
            self.remove()

    def finishing_haircut(self):
        if self.current_hair_cut_length == 0 and self.marked_as_getting_haircut == True:
            self.marked_as_finished_haircut = True
            self.remove()
            print(f"[{str(model.convert_to_hh_mm(model.clock_time))}] Barber {str(self.my_barber)} finished cutting customer {str(self.unique_id)}")
            print(f"[{str(model.convert_to_hh_mm(model.clock_time))}] Customer {str(self.unique_id)} leaves satisfied")
            for agent in self.model.schedule.agents:
                if isinstance(agent, Barber) and agent.my_customer == self.unique_id:
                    agent.my_customer = None
        else:
            self.current_hair_cut_length -= 1

class Barbesrhop_Model(mesa.Model):
    """A model with some number of agents."""

    @staticmethod
    def convert_to_hh_mm(total_minutes):
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"

    def __init__(self, num_Barber):
        super().__init__()
        self.start_time = "09:00"
        hours, minutes = map(int, self.start_time.split(':'))
        self.clock_time = hours * 60 + minutes
        print(f"[{str(self.convert_to_hh_mm(self.clock_time))}] Jesse Boardman's Barbering is open for business.")

        self.schedule = mesa.time.RandomActivation(self)
        self.time = 0
        self.customer_count = 0
        self.longest_waiting_customer_num = 1  # Initialize the longest waiting customer and their waiting time
        self.longest_waiting_time = 0
        self.num_in_waiting_room = 0  # Initialize the waiting room size counter
        self.max_num_in_waiting_room = 1
        self.length_of_shift = 10

        # Create Barber
        self.num_Barber = num_Barber
        for i in range(self.num_Barber):
            a = Barber(i+1, self, None, 0)
            # Add the agent to the scheduler
            self.schedule.add(a)
            print(f"[{str(self.convert_to_hh_mm(self.clock_time))}] Barber {i+1} started shift")


    def step(self):
        """Advance the model by one step."""
        self.create_customer()
        self.assign_customer_to_barber()
        self.find_longest_waiting_customer()
        self.waiting_room()  # Print waiting room size
        self.barber_signs_out() # Barber signs out after working too long
        self.new_barber_signs_in() # New barber signs in
        self.iterate_barbers_time_on_shift()
        self.time += 1  # Increment time
        self.clock_time += 1 #Increment clock time
        self.schedule.step()

    def find_longest_waiting_customer(self):
        # Find the customer with the longest waiting time
        for agent in self.schedule.agents:
            if isinstance(agent,
                          Customer) and agent.time_waiting > self.longest_waiting_time and agent.marked_as_waiting is True:
                self.longest_waiting_customer_num = agent.unique_id
                self.longest_waiting_time = agent.time_waiting
                # print(
                #     f"Longest waiting customer {self.longest_waiting_customer_num} with {self.longest_waiting_time} minutes wait.")

    def assign_customer_to_barber(self):
        # Assign the longest waiting customer to a barber
        for agent in self.schedule.agents:
            if isinstance(agent, Barber) and agent.my_customer is None:
                # print(f"Barber {agent.unique_id} is available!")
                for customer_longest_waiting in self.schedule.agents:
                    if (isinstance(customer_longest_waiting,
                                   Customer) and customer_longest_waiting.unique_id == self.longest_waiting_customer_num
                            and customer_longest_waiting.marked_as_waiting):
                        agent.my_customer = self.longest_waiting_customer_num
                        print(f"[{str(self.convert_to_hh_mm(self.clock_time))}] Barber {agent.unique_id} started cutting customer {agent.my_customer}'s hair.")
                        starting_hair_cut_length = 2  # create length of time of haircut
                        agent.current_hair_cut_length = starting_hair_cut_length
                        customer_longest_waiting.current_hair_cut_length = starting_hair_cut_length
                        customer_longest_waiting.marked_as_waiting = False
                        customer_longest_waiting.marked_as_getting_haircut = True
                        customer_longest_waiting.my_barber = agent.unique_id
                        break

    def iterate_barbers_time_on_shift(self):
        for agent in self.schedule.agents:
            if isinstance(agent, Barber) and agent.on_shift == True:
                agent.time_on_shift += 1
                #print(f"Barber {agent.unique_id} has been working for {agent.time_on_shift} minutes")

    def barber_signs_out(self):
        for agent in self.schedule.agents:
            if isinstance(agent, Barber) and agent.my_customer is None and  agent.time_on_shift > self.length_of_shift:
                agent.on_shift = False
                print(f"[{str(self.convert_to_hh_mm(self.clock_time))}] Barber {agent.unique_id} ended shift")

    def new_barber_signs_in(self):
        for agent in self.schedule.agents:
            if isinstance(agent, Barber) and agent.on_shift == False:
                agent.remove()
                self.num_Barber += 1
                new_barber = Barber(self.num_Barber, self, None, 0)
                # Add the agent to the scheduler
                self.schedule.add(new_barber)
                print(f"[{str(self.convert_to_hh_mm(self.clock_time))}] Barber {self.num_Barber} started shift")

    def create_customer(self):
        if self.time % 3 == 0:
            if self.num_in_waiting_room < self.max_num_in_waiting_room:
                customer = Customer(self.customer_count + 1, self)  # Create a new customer with a unique ID
                self.customer_count += 1  # Increment the customer count for the next customer
                self.schedule.add(customer)
                print(f"[{self.convert_to_hh_mm(self.clock_time)}] Customer {self.customer_count} enters ")
            else:
                # customer = Customer(self.customer_count + 1, self)  # Create a new customer with a unique ID
                self.customer_count += 1  # Increment the customer count for the next customer
                #self.schedule.add(customer)
                print(f"[{self.convert_to_hh_mm(self.clock_time)}] Customer {self.customer_count} leaves unfulfilled ")

    def waiting_room(self):
        self.num_in_waiting_room = sum(1 for agent in self.schedule.agents if isinstance(agent, Customer) and agent.marked_as_waiting)
        # print(f"Waiting room size: {self.num_in_waiting_room}.")

model = Barbesrhop_Model(1)
for i in range(20):
    model.step()
