import heapq

class Passenger:
    def __init__(self, start_station, destination_station, request_time):
        self.start_station = start_station
        self.destination_station = destination_station
        self.request_time = request_time
        self.priority = self.calculate_initial_priority()

    def calculate_initial_priority(self):
        # Calculate initial priority based on distance between start station and destination
        stations = ['A', 'B', 'C', 'D']
        start_index = stations.index(self.start_station)
        dest_index = stations.index(self.destination_station)
        distance = abs(start_index - dest_index)
        return distance

    def recalculate_priority(self, current_station):
        # Recalculate priority based on current station and destination
        stations = ['A', 'B', 'C', 'D']
        current_index = stations.index(current_station)
        dest_index = stations.index(self.destination_station)
        distance = abs(current_index - dest_index)
        self.priority = distance

class Emergency:
    def __init__(self, request_time):
        self.request_time = request_time

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
        while self.passengers:
            priority, passenger = heapq.heappop(self.passengers)
            print(f"Processing passenger from {passenger.start_station} to {passenger.destination_station}")
            if passenger.destination_station == self.current_station:
                print(f"Passenger arrived at destination {passenger.destination_station}")
                self.passengers = [(p.priority, p) for p in self.passengers if p != passenger]
            else:
                passenger.recalculate_priority(self.current_station)
                heapq.heappush(self.passengers, (passenger.priority, passenger))

    def process_emergencies(self):
        while self.emergencies:
            emergency = self.emergencies.pop()
            print(f"Handling emergency at {emergency.request_time}")

    def move_train(self, new_station):
        self.current_station = new_station
        print(f"Train moved to {new_station}")
        self.process_passengers()

    def calculate_average_travel_time(self):
        total_time = 0
        for passenger in self.passengers:
            total_time += passenger.request_time
        return total_time / len(self.passengers)

# Example usage
system = TrainControlSystem()

passenger1 = Passenger('A', 'C', 10)
passenger2 = Passenger('B', 'D', 20)
passenger3 = Passenger('C', 'A', 30)

system.add_passenger(passenger1)
system.add_passenger(passenger2)
system.add_passenger(passenger3)

system.move_train('B')
system.move_train('C')
system.move_train('D')

emergency1 = Emergency(40)
system.add_emergency(emergency1)

system.process_emergencies()

print(f"Average travel time: {system.calculate_average_travel_time()}")