import heapq
import random

stations = ['A', 'B', 'C', 'D']
station_time = 10  # Each station is 10 minutes apart

class Passenger:
    def __init__(self, start_station, destination_station, request_time, is_emergency=False):
        self.start_station = start_station
        self.destination_station = destination_station
        self.request_time = request_time
        self.is_emergency = is_emergency
        self.boarded = False
        self.board_time = None
        self.priority = self.calculate_priority()
        self.total_time_on_train = 0  # To track the total time spent on the train

    def calculate_priority(self):
        start_index = stations.index(self.start_station)
        dest_index = stations.index(self.destination_station)
        distance = abs(start_index - dest_index)
        return 0 if self.is_emergency else distance  # Emergency passengers get the highest priority (0)

    def recalculate_priority(self, current_station):
        current_index = stations.index(current_station)
        dest_index = stations.index(self.destination_station)
        distance = abs(current_index - dest_index)
        self.priority = 0 if self.is_emergency else distance

    def __lt__(self, other):
        return self.priority < other.priority

class TrainControlSystem:
    def __init__(self):
        self.passengers = []
        self.current_station = 'A'
        self.current_time = 0  # Time starts at 0 minutes
        self.total_travel_time = 0  # Track total travel time globally
        self.waiting_passengers = []  # Passengers waiting at stations

    def add_passenger(self, passenger):
        self.waiting_passengers.append(passenger)  # Passengers wait at their stations initially

    def process_passengers(self):
        if self.passengers:
            priority, passenger = heapq.heappop(self.passengers)
            print(f"Processing passenger from {passenger.start_station} to {passenger.destination_station} at {self.current_time} minutes")
            if passenger.destination_station == self.current_station:
                print(f"Passenger arrived at destination {passenger.destination_station} at {self.current_time} minutes")
                travel_time = self.current_time - passenger.board_time + station_time  # Add the baseline 10 minutes
                self.total_travel_time += travel_time
                print(f"Passenger spent {travel_time} minutes on the train")
            else:
                passenger.recalculate_priority(self.current_station)
                heapq.heappush(self.passengers, (passenger.priority, passenger))

    def move_train(self, new_station):
        travel_time = station_time * abs(stations.index(self.current_station) - stations.index(new_station))
        self.current_time += travel_time
        print(f"Train moved to {new_station} at {self.current_time} minutes")

        # Update the time for each passenger currently on the train
        for priority, passenger in self.passengers:
            passenger.total_time_on_train += travel_time  # Add travel time to passengers still on the train

        self.current_station = new_station
        self.board_passengers()  # Passengers at this station can now board
        self.process_passengers()

    def board_passengers(self):
        for passenger in self.waiting_passengers[:]:
            if passenger.start_station == self.current_station:
                print(f"Passenger from {passenger.start_station} to {passenger.destination_station} boarded at {self.current_time} minutes")
                passenger.board_time = self.current_time  # Track when the passenger boards the train
                passenger.boarded = True
                heapq.heappush(self.passengers, (passenger.priority, passenger))
                self.waiting_passengers.remove(passenger)

    def run_simulation(self, num_runs=10):
        total_passengers = 0
        total_time_spent = 0  # Initialize total time spent by all passengers

        for run in range(num_runs):
            print(f"--- Simulation Run {run + 1} ---")
            self.current_station = 'A'
            self.current_time = 0
            self.passengers = []
            self.waiting_passengers = []
            run_total_travel_time = 0  # Reset total travel time for this run

            # Generate random passengers for each run
            num_passengers = random.randint(3, 5)  # Random number of passengers per run
            total_passengers += num_passengers
            for _ in range(num_passengers):
                start_station = random.choice(stations)
                dest_station = random.choice(stations)
                while dest_station == start_station:
                    dest_station = random.choice(stations)  # Ensure start != destination

                request_time = random.randint(1, 50)
                is_emergency = random.choice([False, True])  # Randomly decide if it's an emergency
                passenger = Passenger(start_station, dest_station, request_time, is_emergency)
                print(f"Passenger from {start_station} to {dest_station}, "
                      f"Priority: {passenger.priority}, Emergency: {is_emergency}")
                self.add_passenger(passenger)

            # Simulate train movement through all stations
            for station in stations:
                self.move_train(station)

            # After simulation, sum up total travel time for passengers still on board
            for priority, passenger in self.passengers:
                run_total_travel_time += passenger.total_time_on_train + station_time  # Ensure baseline time is added

            total_time_spent += run_total_travel_time
            print(f"Total travel time for this run: {run_total_travel_time} minutes\n")
            average_time_passengers = total_time_spent / total_passengers

        return total_time_spent, total_passengers, average_time_passengers

# Example usage
system = TrainControlSystem()

# Run 10 simulation runs
total_time, total_passengers, average_time_passengers = system.run_simulation(10)
print(f"\nTotal time spent by all passengers: {total_time} minutes")
print(f"Total number of passengers: {total_passengers}")
print(f"{average_time_passengers:.2f} Minutes spent per passenger on average")
