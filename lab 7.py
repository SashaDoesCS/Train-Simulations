import random


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None

    def push(self, passenger):
        new_node = Node(passenger)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top:
            top_passenger = self.top.data
            self.top = self.top.next
            return top_passenger
        return None

    def is_empty(self):
        return self.top is None

    def peek(self):
        return self.top.data if self.top else None


class LinkedList:
    def __init__(self):
        self.head = None

    def add_in_priority_order(self, passenger):
        new_node = Node(passenger)
        # Emergency passengers always go to emergency stack, so this is only for regular passengers
        if not self.head:
            self.head = new_node
            return

        # If new passenger should be first
        if self.head.data.calculate_distance() > passenger.calculate_distance():
            new_node.next = self.head
            self.head = new_node
            return

        # Find position for new passenger
        current = self.head
        while current.next and current.next.data.calculate_distance() <= passenger.calculate_distance():
            current = current.next
        new_node.next = current.next
        current.next = new_node

    def pop(self):
        if self.head:
            top_passenger = self.head.data
            self.head = self.head.next
            return top_passenger
        return None

    def is_empty(self):
        return self.head is None


class Passenger:
    def __init__(self, id, start_station, destination_station, request_time, is_emergency=False):
        self.id = id
        self.start_station = start_station
        self.destination_station = destination_station
        self.request_time = request_time
        self.is_emergency = is_emergency
        self.boarded = False
        self.board_time = None
        self.total_time_on_train = 0
        self.completed = False

    def calculate_distance(self):
        """Calculate the distance between start and destination stations"""
        start_index = stations.index(self.start_station)
        dest_index = stations.index(self.destination_station)
        distance = abs(start_index - dest_index)
        return distance if not self.is_emergency else 0

    def __str__(self):
        status = "🚨 Emergency" if self.is_emergency else "Regular"
        return f"{status} Passenger {self.id}: {self.start_station} → {self.destination_station}"


class TrainControlSystem:
    def __init__(self):
        self.normal_passenger_queue = LinkedList()
        self.emergency_stack = Stack()
        self.current_station = 'A'
        self.current_time = 0
        self.active_passengers = []
        self.completed_passengers = []
        self.passenger_id_counter = 0
        self.total_passengers_generated = 0
        self.stops_made = 0
        self.emergency_passengers_served = 0
        self.regular_passengers_served = 0

    def get_next_station(self):
        current_index = stations.index(self.current_station)
        return stations[(current_index + 1) % len(stations)]

    def generate_passenger(self, station):
        possible_destinations = [s for s in stations if s != station]
        if not possible_destinations:
            return None

        destination = random.choice(possible_destinations)
        is_emergency = random.random() < 0.2  # 20% chance of emergency

        self.passenger_id_counter += 1
        new_passenger = Passenger(
            id=self.passenger_id_counter,
            start_station=station,
            destination_station=destination,
            request_time=self.current_time,
            is_emergency=is_emergency
        )

        if is_emergency:
            self.emergency_stack.push(new_passenger)
            print(f"Generated: {new_passenger}")
        else:
            self.normal_passenger_queue.add_in_priority_order(new_passenger)
            print(f"Generated: {new_passenger}")

        self.total_passengers_generated += 1
        return new_passenger

    def process_passengers(self):
        # First handle passengers reaching their destination
        remaining_passengers = []
        for passenger in self.active_passengers:
            if passenger.destination_station == self.current_station:
                passenger.completed = True
                travel_time = self.current_time - passenger.board_time
                passenger.total_time_on_train = travel_time
                self.completed_passengers.append(passenger)
                if passenger.is_emergency:
                    self.emergency_passengers_served += 1
                else:
                    self.regular_passengers_served += 1
                print(f"✓ {passenger} completed journey in {travel_time} minutes")
            else:
                remaining_passengers.append(passenger)
        self.active_passengers = remaining_passengers

        # Process ONLY emergency passengers if any exist
        if not self.emergency_stack.is_empty():
            self._handle_emergency_passengers()
        else:
            # Only process regular passengers if no emergencies
            self._handle_regular_passengers()

    def _handle_emergency_passengers(self):
        while not self.emergency_stack.is_empty():
            passenger = self.emergency_stack.pop()
            if passenger.start_station == self.current_station and not passenger.boarded:
                passenger.boarded = True
                passenger.board_time = self.current_time
                self.active_passengers.append(passenger)
                print(f"↑ {passenger} boarded")

    def _handle_regular_passengers(self):
        while not self.normal_passenger_queue.is_empty():
            passenger = self.normal_passenger_queue.pop()
            if passenger.start_station == self.current_station and not passenger.boarded:
                passenger.boarded = True
                passenger.board_time = self.current_time
                self.active_passengers.append(passenger)
                print(f"↑ {passenger} boarded")

    def move_train(self):
        if self.stops_made >= 20:
            return False

        new_station = self.get_next_station()
        travel_time = station_time
        self.current_time += travel_time
        self.stops_made += 1

        print(
            f"\n=== Stop {self.stops_made}/20: {self.current_station} → {new_station} (Time: {self.current_time}) ===")

        if not self.emergency_stack.is_empty():
            print("❗ Emergency passengers waiting - prioritizing emergency stack")

        self.current_station = new_station

        # Generate new passengers before processing
        self.generate_passengers_at_station(new_station)
        self.process_passengers()

        # Print current train status
        self._print_train_status()
        return True

    def generate_passengers_at_station(self, station):
        num_passengers = random.randint(1, 3)
        print(f"\nGenerating {num_passengers} passengers at Station {station}:")
        for _ in range(num_passengers):
            self.generate_passenger(station)

    def _print_train_status(self):
        if self.active_passengers:
            print("\nCurrent passengers on train:")
            for passenger in self.active_passengers:
                print(f"• {passenger}")
        else:
            print("\nTrain is empty")

        if not self.emergency_stack.is_empty():
            print("\nEmergency passengers waiting in stack:")
            current = self.emergency_stack.top
            while current:
                print(f"! {current.data}")
                current = current.next

    def run_simulation(self, num_runs=10):
        total_time_all_runs = 0
        total_emergency_passengers = 0
        total_regular_passengers = 0

        for run in range(num_runs):
            print(f"\n{'=' * 20} Run {run + 1} {'=' * 20}")
            self.__init__()

            # Run for exactly 20 stops
            while self.stops_made < 20:
                if not self.move_train():
                    break

            # Calculate statistics for this run
            run_completed_passengers = len(self.completed_passengers)
            run_total_time = sum(p.total_time_on_train for p in self.completed_passengers)

            print(f"\nRun {run + 1} Summary:")
            print(f"Total stops made: {self.stops_made}")
            print(f"Emergency passengers served: {self.emergency_passengers_served}")
            print(f"Regular passengers served: {self.regular_passengers_served}")
            print(f"Total passengers completed: {run_completed_passengers}")

            if run_completed_passengers > 0:
                avg_time = run_total_time / run_completed_passengers
                print(f"Average journey time: {avg_time:.1f} minutes")

            total_time_all_runs += run_total_time
            total_emergency_passengers += self.emergency_passengers_served
            total_regular_passengers += self.regular_passengers_served

        return total_time_all_runs, total_emergency_passengers, total_regular_passengers


# Constants
stations = ['A', 'B', 'C', 'D']
station_time = 10  # minutes between stations

# Run simulation
if __name__ == "__main__":
    system = TrainControlSystem()
    total_time, total_emergency, total_regular = system.run_simulation(num_runs=10)
    print("\n=== Overall Simulation Results ===")
    print(f"Total emergency passengers served: {total_emergency}")
    print(f"Total regular passengers served: {total_regular}")
    print(f"Total travel time: {total_time} minutes")
    if (total_emergency + total_regular) > 0:
        avg_time = total_time / (total_emergency + total_regular)
        print(f"Overall average journey time: {avg_time:.1f} minutes")
