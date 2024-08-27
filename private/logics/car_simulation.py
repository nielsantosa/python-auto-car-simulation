from private.models.car import Car
from private.models.field import Field
from private.models.position import Position
from private.constants.constants import DirectionEnum
import time
import os

# For drawing
BOARD_DICT = {
    DirectionEnum.N: "[↑]",
    DirectionEnum.E: "[→]",
    DirectionEnum.S: "[↓]",
    DirectionEnum.W: "[←]"
}
EMPTY = "[ ]"
COLLIDED = "[X]"

class CarSimulationLogic:
    def __init__(self, field: Field = Field(10, 10), cars: list[Car] = []):
        self.field = field
        self.cars = cars
        self.car_collision_list: dict[int, list[Car]] = {}

    def draw_board(self, step):
        """
        Draw something like this :
        0 0 ↑ O O
        O O O → O
        O O O O O
        O O O O O
        """
        # os.system("clear")

        positions_dict: dict[str, Car] = {}
        for car in self.cars:
            positions_dict[str(car.position)] = car

        print(f"Step {step}...")
        for i in range(self.field.height - 1, -1, -1):
            row = []
            for j in range(self.field.width):
                key = f"({j},{i})"
                if key in positions_dict:
                    c = positions_dict[key]
                    if c.is_collision:
                        row.append(COLLIDED)
                    else:
                        row.append(BOARD_DICT[positions_dict[key].facing])
                else:
                    row.append(EMPTY)
            print(" ".join(row))
        print()

    def run_simulation(self):
        """
        Run simulation
        If got collisions, stop the car for the rest of the simulation
        """
        total_steps = self.get_total_steps()
        self.initialize_car_list_validity()
        self.draw_board(0)
        for step in range(1, total_steps + 1):
            for car in [c for c in self.cars if not c.is_collision]:
                if car.is_collision:
                    continue

                if step > len(car.commands):
                    continue

                command = car.commands[step - 1]
                new_position = car.run_command(command, step)

                if new_position != car.position and not self.is_colliding_out_of_bound(
                    step, car, new_position
                ):
                    car.position = new_position

            time.sleep(0.8)
            self.draw_board(step)

    def is_colliding_out_of_bound(
        self, step: int, car: Car, new_position: Position
    ) -> bool:
        return self.is_colliding(car, step, new_position) or not self.is_within_bounds(
            new_position
        )

    def initialize_car_list_validity(self):
        for car in self.cars:
            self.is_colliding_out_of_bound(0, car, car.position)

    def get_total_steps(self) -> int:
        max_commands = max(len(car.commands) for car in self.cars)
        return max_commands

    def is_colliding(self, current_car: Car, step: int, new_position: Position) -> bool:
        """
        Criteria for collision:
            1. Move to a Position where there are existing car
        """
        car_list: list[Car] = self.car_collision_list.get(step, [])
        step_collision_status: bool = False

        for car in self.cars:
            if car.name != current_car.name and car.position == new_position:
                car.is_collision = True
                current_car.is_collision = True
                current_car.position = (
                    new_position  # To ensure the collided cars are in the same position
                )
                step_collision_status = True
                if car not in car_list:
                    car_list.append(car)
                if current_car not in car_list:
                    car_list.append(current_car)

        self.car_collision_list[step] = car_list
        return step_collision_status

    def is_within_bounds(self, position: Position) -> bool:
        return (
            0 <= position.x < self.field.width and 0 <= position.y < self.field.height
        )

    def clear(self):
        self.cars.clear()
        self.car_collision_list.clear()
