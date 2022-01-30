from time import sleep
from random import randint


class Building:

    def __init__(self):
        super(Building, self).__init__()
        n = randint(5, 20)
        print(f"Created a building with {n} floors")
        self.number_of_floors = n
        self.elevator = PassengerElevator(self.number_of_floors)

    def generate_simulation(self) -> list:
        """Generates a new simulation with current configuration settings."""
        passengers_list = []

        for i in range(1, self.number_of_floors + 1):
            start_floor = i
            # Генерируем случайное количество людей на этаже.
            k = randint(0, 10)
            print(f"floor {i} with {k} people")
            # Создаём этаж на который человеку нужно.
            for j in range(k):
                while True:
                    target_floor = randint(1, self.number_of_floors)
                    if start_floor != target_floor:
                        break
                # Рассчитываем какую кнопку человек нажмёт.
                if target_floor - start_floor > 0:
                    button = "Up"
                else:
                    button = "Down"
                # Adds the person dictionary to the list.

                person = {
                    "id": len(passengers_list),
                    "start_floor": start_floor,
                    "target_floor": target_floor,
                    "button": button,
                }
                passengers_list.append(person)

        return passengers_list

    def run_simulation(self, passengers_list) -> None:
        passenger_objects = []

        for i in range(len(passengers_list)):
            new_pass = Passenger(passengers_list[i])
            passenger_objects.append(new_pass)

        while len(passenger_objects) > 0:
            sleep(1)
            print(f"Floor {self.elevator.floor}")
            print("________________________________________")
            # Перебираем пассажиров в лифте на этаже
            for passenger in self.elevator.passengers:
                if passenger:
                    print("|                  0                    |")
            print("________________________________________")
            # Перебираем пассажиров в лифте на этаже
            for passenger in self.elevator.passengers:
                # Если этаж пассажира совпадает с текущим, он выходит и выпадает из списка лифта и списка объектов
                if passenger.target_floor == self.elevator.floor:
                    pass_index = passenger.id
                    print(f"Passenger {pass_index} has arrived")
                    self.elevator.passengers.remove(passenger)
                    for obj in passenger_objects:
                        if obj.id == pass_index:
                            target_floor = randint(1, self.number_of_floors)
                            if obj.start_floor == target_floor:
                                passenger_objects.remove(obj)

            # Выбираем пассажира
            for passenger in passenger_objects:
                # Может ли лифт взять нового пассажира
                if len(self.elevator.passengers) < self.elevator.max_passengers:
                    # Если пассажир на этаже:
                    if passenger.start_floor == self.elevator.floor:
                        # Если лифт едет с пассажирами
                        if len(self.elevator.passengers) > 0:
                            # Если пассажиру наверх
                            if passenger.button == 'Up' and self.elevator.up:
                                # Пассажир заходит в лифт
                                print(
                                    f"Passеnger {passenger.id} entered, {passenger.button}, {passenger.target_floor}")
                                self.elevator.passengers.append(passenger)
                            # Если пассажиру вниз
                            if passenger.button == 'Down' and not self.elevator.up:
                                # Пассажир заходит в лифт
                                print(
                                    f"Passеnger {passenger.id} entered, {passenger.button}, {passenger.target_floor}")
                                self.elevator.passengers.append(passenger)
                        else:
                            # Если лифт пуст, пассажир едет по назначению
                            print(f"Passеnger {passenger.id} entered, {passenger.button}, {passenger.target_floor}")
                            self.elevator.passengers.append(passenger)
                            if self.elevator.passengers[0].button == 'Up':
                                self.elevator.up = True
                            else:
                                self.elevator.up = False

            if self.elevator.up:
                # Разворот на последнем этаже
                if self.elevator.floor == self.number_of_floors:
                    self.elevator.up = False
                    print("Elevator going down")
                    next_floor = self.elevator.floor - 1
                else:
                    print("Elevator going up")
                    next_floor = self.elevator.floor + 1
                    # Если лифт полон
                    if len(self.elevator.passengers) == self.elevator.max_passengers:
                        next_floor = self.elevator.passengers[0].target_floor
                        for passenger in self.elevator.passengers:
                            if passenger.target_floor <= next_floor:
                                next_floor = passenger.target_floor
                        print(f"Elevator is full and going up to {next_floor} floor")

            else:
                # Разворот на первом этаже
                if self.elevator.floor == 1:
                    self.elevator.up = True
                    print("Elevator going up")
                    next_floor = self.elevator.floor + 1
                else:
                    print("Elevator going down")
                    next_floor = self.elevator.floor - 1
                    # Если лифт полон
                    if len(self.elevator.passengers) == self.elevator.max_passengers:
                        next_floor = self.elevator.passengers[0].targer_floor
                        for passenger in self.elevator.passengers:
                            if passenger.target_floor >= next_floor:
                                next_floor = passenger.target_floor
                        print(f"Elevator is full and going down to {next_floor} floor")

            self.elevator.move(next_floor)
            print(f"{len(self.elevator.passengers)} passengers. Next floor {self.elevator.floor}")


class Elevator:

    def __init__(self, max_floor):
        self.floor = 1
        self.max_floor = max_floor
        self.up = True

    def move(self, floor):
        if floor > self.floor:
            vector = 1
        else:
            vector = -1
        while self.floor != floor:
            self.floor += vector


class PassengerElevator(Elevator):
    max_passengers = 5
    passengers = []


class Passenger:

    def __init__(self, passenger):
        self.id = passenger['id']
        self.start_floor = passenger['start_floor']
        self.target_floor = passenger['target_floor']
        self.button = passenger['button']


if __name__ == '__main__':
    building = Building()
    pass_list = building.generate_simulation()

    for p in range(len(pass_list)):
        print(pass_list[p])

    building.run_simulation(pass_list)

    print("End of simulation")
