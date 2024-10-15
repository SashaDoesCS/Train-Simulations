import heapq

stations = ['A', 'B', 'C', 'D']

class Passenger:
    def __init__(self, start_station, destination_station, request_time):
        self.start_station = start_station
        self.destination_station = destination_station
        self.request_time = request_time
        self.priority = self.calculate_priority()

    def calculate_priority(self):
        start_index = stations.index(self.start_station)
        dest_index = stations.index(self.destination_station)
        distance = abs(start_index - dest_index)
        return distance

    def recalculate_priority(self, current_station):
        current_index = stations.index(current_station)
        dest_index = stations.index(self.destination_station)
        distance = abs(current_index - dest_index)
        self.priority = distance

    def __lt__(self, other):
        return self.priority < other.priority

class PassengerQueue:
    def __init__(self):
        self.queue = []
        self.current_station = 'A'

    def add_passenger(self, passenger):
        heapq.heappush(self.queue, passenger)

    def update_priority(self):
        passengers = []
        while self.queue:
            passenger = heapq.heappop(self.queue)
            passenger.recalculate_priority(self.current_station)
            passengers.append(passenger)

        for passenger in passengers:
            heapq.heappush(self.queue, passenger)

    def add_next_passenger(self):
        if self.queue:
            return heapq.heappop(self.queue)
        return None

class Emergency:
    def __init__(self, station, request_time, description):
        self.station = station
        self.request_time = request_time
        self.description = description

class TrainControlSystem:
    def __init__(self):
        self.passengers = []
        self.emergencies = []
        self.current_station = 'A'

    def add_passenger(self, passenger):
        heapq.heappush(self.passengers, (passenger.priority, passenger))

    def add_emergency(self, emergency):
        self.emergencies.append(emergency)

    def process_passengers(self):
        # Process emergencies first
        if self.emergencies:
            self.process_emergencies()

        # Process passengers
        if self.passengers:
            priority, passenger = heapq.heappop(self.passengers)
            print(f"Processing passenger from {passenger.start_station} to {passenger.destination_station}")
            if passenger.destination_station == self.current_station:
                print(f"Passenger arrived at destination {passenger.destination_station}")
            else:
                # Recalculate priority and re-add if passenger hasn't reached destination
                passenger.recalculate_priority(self.current_station)
                heapq.heappush(self.passengers, (passenger.priority, passenger))

    def process_emergencies(self):
        while self.emergencies:
            emergency = self.emergencies.pop(0)  # Handle the first emergency in the list
            print(f"Handling emergency at station {emergency.station} at time {emergency.request_time}: {emergency.description}")
            self.move_train(emergency.station)  # Move the train to the emergency location immediately

    def move_train(self, new_station):
        self.current_station = new_station
        self.visualize_train_position()  # Visualize the train at the new station
        print(f"Train moved to {new_station}")
        self.process_passengers()

    def visualize_train_position(self):
        # Create a simple text-based visualization of the train and stations
        train_position = stations.index(self.current_station)
        station_display = ["[T]" if i == train_position else f"[{station}]" for i, station in enumerate(stations)]
        print(" ".join(station_display))

    def calculate_average_travel_time(self):
        total_time = 0
        for _, passenger in self.passengers:
            total_time += passenger.request_time
        if self.passengers:
            return total_time / len(self.passengers)
        return 0

# Example usage
system = TrainControlSystem()

passenger1 = Passenger('A', 'C', 10)
passenger2 = Passenger('B', 'D', 20)
passenger3 = Passenger('C', 'A', 30)

system.add_passenger(passenger1)
system.add_passenger(passenger2)
system.add_passenger(passenger3)

# Emergency example with a description
emergency1 = Emergency('D', 40, "Fire reported in station D")
system.add_emergency(emergency1)

# Visualize the train moving through stations
system.move_train('B')
system.move_train('C')
system.process_emergencies()  # Handle emergencies first
system.move_train('D')  # Continue with regular passengers

print(f"Average travel time: {system.calculate_average_travel_time()}")
