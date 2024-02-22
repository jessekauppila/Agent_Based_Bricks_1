import mesa
import random
from barber import Barber
from customer import Customer

class Barbershop_Model(mesa.Model):
    """A model with some number of agents."""

    @staticmethod
    def convert_to_hh_mm(total_minutes):
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"

    def __init__(self, num_Barber, max_num_in_waiting_room, length_of_shift, min_haircut_length, max_haircut_length, closing_time, rate_of_customers):
        super().__init__()
        self.schedule = mesa.time.RandomActivation(self)

        self.start_time = "09:00"
        hours, minutes = map(int, self.start_time.split(':'))
        self.clock_time = hours * 60 + minutes
        print(f"[{str(self.convert_to_hh_mm(self.clock_time))}] Jesse Boardman's Barbering is open for business.")

        self.num_Barber = num_Barber
        for i in range(self.num_Barber):
            a = Barber(i+1, self, None, 0)
            # Add the agent to the scheduler
            self.schedule.add(a)
            print(f"[{str(self.convert_to_hh_mm(self.clock_time))}] Barber {i+1} started shift")
        self.max_num_in_waiting_room = max_num_in_waiting_room
        self.length_of_shift = length_of_shift
        self.min_haircut_length = min_haircut_length
        self.max_haircut_length = max_haircut_length
        self.random_haircut_length = random.randint(self.min_haircut_length, self.max_haircut_length)
        self.closing_time = closing_time
        self.rate_of_customers = rate_of_customers

        self.marked_as_open = True
        self.time = 0
        self.customer_count = 0
        self.longest_waiting_customer_num = 1  # Initialize the longest waiting customer and their waiting time
        self.longest_waiting_time = 0
        self.num_in_waiting_room = 0  # Initialize the waiting room size counter

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
        self.closing()

    def find_longest_waiting_customer(self):
        # Find the customer with the longest waiting time
        for agent in self.schedule.agents:
            if isinstance(agent,
                          Customer) and agent.time_waiting > self.longest_waiting_time and agent.marked_as_waiting is True:
                self.longest_waiting_customer_num = agent.unique_id
                self.longest_waiting_time = agent.time_waiting
                print(f"Longest waiting customer is {self.longest_waiting_customer_num}")

    def assign_customer_to_barber(self):
        # Assign the longest waiting customer to a barber6
        for agent in self.schedule.agents:
            if isinstance(agent, Barber) and agent.my_customer is None:
                # print(f"Barber {agent.unique_id} is available!")
                for customer_longest_waiting in self.schedule.agents:
                    if (isinstance(customer_longest_waiting,
                                   Customer) and customer_longest_waiting.unique_id == self.longest_waiting_customer_num
                            and customer_longest_waiting.marked_as_waiting):
                        agent.my_customer = self.longest_waiting_customer_num
                        print(f"[{str(self.convert_to_hh_mm(self.clock_time))}] Barber {agent.unique_id} started cutting customer {agent.my_customer}'s hair.")
                        agent.current_hair_cut_length = self.random_haircut_length
                        customer_longest_waiting.current_hair_cut_length = self.random_haircut_length
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
            if isinstance(agent, Barber) and agent.my_customer is None and  agent.time_on_shift > self.length_of_shift and agent.on_shift == True:
                agent.on_shift = False
                #agent.remove()
                print(f"[{str(self.convert_to_hh_mm(self.clock_time))}] Barber {agent.unique_id} ended shift")

    def new_barber_signs_in(self):
        for agent in self.schedule.agents:
            if isinstance(agent, Barber) and agent.on_shift == False and self.marked_as_open == True:
                agent.remove()
                self.num_Barber += 1
                new_barber = Barber(self.num_Barber, self, None, 0)
                # Add the agent to the scheduler
                self.schedule.add(new_barber)
                print(f"[{str(self.convert_to_hh_mm(self.clock_time))}] Barber {self.num_Barber} started shift")


    def create_customer(self):
        if self.time % self.rate_of_customers == 0:
            if self.num_in_waiting_room < self.max_num_in_waiting_room and self.time < self.closing_time:
                customer = Customer(self.customer_count + 1, model, model)  # Create a new customer with a unique ID

                self.customer_count += 1  # Increment the customer count for the next customer
                self.schedule.add(customer)
                print(f"[{self.convert_to_hh_mm(self.clock_time)}] Customer {self.customer_count} enters ")
            elif self.time > self.closing_time:
                #customer comes in, but the waiting room is full.
                self.customer_count += 1
                print(f"[{self.convert_to_hh_mm(self.clock_time)}] Customer {self.customer_count} leaves unfulfilled ")

    def closing(self):
        if self.time > self.closing_time and self.marked_as_open == True:
            print(f"[{self.convert_to_hh_mm(self.clock_time)}] Jesse Boardman's Barbering is closed")
            for agent in self.schedule.agents:
                if isinstance(agent,Customer) and agent.marked_as_waiting is True:
                    print(f"[{self.convert_to_hh_mm(self.clock_time)}] Customer {str(agent.unique_id)} leaves cursing")
                    agent.marked_as_waiting = False
            self.marked_as_open = False

    def waiting_room(self):
        self.num_in_waiting_room = sum(1 for agent in self.schedule.agents if isinstance(agent, Customer) and agent.marked_as_waiting)
        # print(f"Waiting room size: {self.num_in_waiting_room}.")

model = Barbershop_Model(4,8,240, 20, 40, 480, 5)
for i in range(600):
    model.step()
