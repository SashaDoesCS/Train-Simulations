# Aided using ChatGPT 4o

import heapq
import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Passenger:
    start_station: str
    destination_station: str
    arrival_time: int
    is_emergency: bool = False
    is_on_train: bool = False
    total_time: int = 0
    passenger_id: int = 0

    def calculate_priority(self) -> int:
        """Calculate passenger priority based on the distance to destination."""
        return abs(ord(self.destination_station) - ord(self.start_station))

    def calculate_journey_time(self, minutes_per_station: int, stations: List[str]) -> int:
        """Calculate the journey time based on stations between start and destination."""
        start_idx = stations.index(self.start_station)
        dest_idx = stations.index(self.destination_station)
        stations_traveled = abs(dest_idx - start_idx)
        return stations_traveled * minutes_per_station


class EmergencyStack:
    def __init__(self):
        self.stack = []

    def push(self, passenger: Passenger):
        self.stack.append(passenger)

    def pop(self) -> Optional[Passenger]:
        return self.stack.pop() if self.stack else None

    def peek(self) -> Optional[Passenger]:
        return self.stack[-1] if self.stack else None

    def is_empty(self) -> bool:
        return len(self.stack) == 0


class TrainSystem:
    def __init__(self):
        self.emergency_stack = EmergencyStack()
        self.regular_passengers = []
        self.current_station = 'A'
        self.direction = 1
        self.current_time = 0
        self.stations = ['A', 'B', 'C', 'D']
        self.completed_passengers = []
        self.minutes_per_station = 10
        self.passenger_counter = 0

    def determine_next_station(self) -> str:
        """Determine the next station the train will go to, prioritizing emergencies."""
        current_idx = self.stations.index(self.current_station)

        # Prioritize emergency passengers
        if not self.emergency_stack.is_empty():
            emergency_passenger = self.emergency_stack.peek()
            emergency_idx = self.stations.index(emergency_passenger.destination_station)
            if emergency_idx > current_idx:
                return self.stations[current_idx + 1]
            elif emergency_idx < current_idx:
                return self.stations[current_idx - 1]

        # If no emergency passengers, check regular passengers
        if self.regular_passengers:
            passengers = [p for _, _, p in self.regular_passengers]
            destinations = [p.destination_station for p in passengers]

            forward_count = sum(1 for dest in destinations if self.stations.index(dest) > current_idx)
            backward_count = sum(1 for dest in destinations if self.stations.index(dest) < current_idx)

            if forward_count >= backward_count and current_idx < len(self.stations) - 1:
                return self.stations[current_idx + 1]
            elif backward_count > forward_count and current_idx > 0:
                return self.stations[current_idx - 1]

        # Default behavior if no passengers or equal distance
        next_idx = current_idx + self.direction
        if next_idx >= len(self.stations) or next_idx < 0:
            self.direction *= -1
            next_idx = current_idx + self.direction
        return self.stations[next_idx]

    def generate_random_passengers(self) -> List[Passenger]:
        """Generate a random number of passengers at the current station."""
        num_passengers = random.randint(0, 2)
        new_passengers = []

        for _ in range(num_passengers):
            self.passenger_counter += 1
            possible_destinations = [s for s in self.stations if s != self.current_station]
            destination = random.choice(possible_destinations)
            is_emergency = random.random() < 0.1

            passenger = Passenger(
                start_station=self.current_station,
                destination_station=destination,
                arrival_time=self.current_time,  # This is when they arrive at the station
                is_emergency=is_emergency,
                passenger_id=self.passenger_counter
            )

            passenger_type = "Emergency" if is_emergency else "Regular"
            print(f"\n{passenger_type} Passenger #{passenger.passenger_id} appears at Station {self.current_station}")
            print(f"   Destination: Station {passenger.destination_station}")

            if is_emergency:
                self.emergency_stack.push(passenger)
                print(f"   ⚡ Added to emergency stack")
            else:
                heapq.heappush(self.regular_passengers, (passenger.calculate_priority(), id(passenger), passenger))
                print(f"   Added to regular queue")

            new_passengers.append(passenger)

        return new_passengers

    def print_status(self):
        """Print the current status of the train, including passengers onboard."""
        print(f"\nTime: {self.current_time} minutes")
        print(f"Current Station: {self.current_station}")

        if not self.emergency_stack.is_empty():
            print("\n⚡ Emergency Passengers on Train:")
            for p in reversed(self.emergency_stack.stack):
                print(f"   Passenger #{p.passenger_id} → Station {p.destination_station}")

        if self.regular_passengers:
            print("\nRegular Passengers on Train:")
            for _, _, p in sorted(self.regular_passengers):
                print(f"   Passenger #{p.passenger_id} → Station {p.destination_station}")

        print("-" * 50)

    def simulate(self, num_stops: int = 20):
        """Simulate the train system for a given number of stops."""
        stops_made = 0

        while stops_made < num_stops:
            self.print_status()

            # Handle emergency passengers first
            while not self.emergency_stack.is_empty():
                emergency_passenger = self.emergency_stack.peek()
                if emergency_passenger.destination_station == self.current_station:
                    completed_passenger = self.emergency_stack.pop()
                    # Calculate total time as current time minus arrival time
                    completed_passenger.total_time = self.current_time - completed_passenger.arrival_time
                    self.completed_passengers.append(completed_passenger)
                    print(f"\n🔴 Emergency Passenger #{completed_passenger.passenger_id} disembarks at Station {self.current_station}")
                    print(f"   Total journey time: {completed_passenger.total_time} minutes")
                else:
                    break

            # Handle regular passengers
            temp_queue = []
            while self.regular_passengers:
                priority, pid, passenger = heapq.heappop(self.regular_passengers)
                if passenger.destination_station == self.current_station:
                    # Calculate total time as current time minus arrival time
                    passenger.total_time = self.current_time - passenger.arrival_time
                    self.completed_passengers.append(passenger)
                    print(f"\nRegular Passenger #{passenger.passenger_id} disembarks at Station {self.current_station}")
                    print(f"   Total journey time: {passenger.total_time} minutes")
                else:
                    temp_queue.append((priority, pid, passenger))

            for item in temp_queue:
                heapq.heappush(self.regular_passengers, item)

            # Generate new passengers at current station
            self.generate_random_passengers()

            # Move to next station
            next_station = self.determine_next_station()
            if next_station != self.current_station:
                print(f"\nTrain moving from Station {self.current_station} to Station {next_station}")
                self.current_station = next_station
                self.current_time += self.minutes_per_station

            stops_made += 1

        print("\n🏁 Simulation complete!")
        print(self.calculate_statistics())

    def calculate_statistics(self):
        """Calculate and return statistics on the journey times of passengers."""
        if not self.completed_passengers:
            return "No passengers completed their journey"

        total_time = sum(p.total_time for p in self.completed_passengers)
        avg_time = total_time / len(self.completed_passengers)
        emergency_passengers = [p for p in self.completed_passengers if p.is_emergency]
        regular_passengers = [p for p in self.completed_passengers if not p.is_emergency]

        stats = f"\n📊 Final Statistics:\n"
        stats += f"Total passengers served: {len(self.completed_passengers)}\n"
        stats += f"Average journey time: {avg_time:.1f} minutes\n"
        stats += f"Emergency passengers: {len(emergency_passengers)}\n"
        stats += f"Regular passengers: {len(regular_passengers)}\n"

        if emergency_passengers:
            avg_emergency_time = sum(p.total_time for p in emergency_passengers) / len(emergency_passengers)
            stats += f"Average emergency journey time: {avg_emergency_time:.1f} minutes\n"

        if regular_passengers:
            avg_regular_time = sum(p.total_time for p in regular_passengers) / len(regular_passengers)
            stats += f"Average regular journey time: {avg_regular_time:.1f} minutes\n"

        return stats


# Run simulation
if __name__ == "__main__":
    train_system = TrainSystem()
    train_system.simulate(20)
