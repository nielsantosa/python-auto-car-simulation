from private.constants.constants import CommandEnum, DirectionEnum
from private.logics.car_simulation import CarSimulationLogic
from private.logics.input_parser import InputParser
from private.models.car import Car
from private.models.field import Field
from private.models.position import Position


class CarSimulation:
    def __init__(self):
        self.parser: InputParser = InputParser()
        self.simulation = CarSimulationLogic()

    def _get_field(self):
        while True:
            print(
                "Please enter the width and height of the simulation field in x y format:"
            )
            raw_input: str = input()
            res, err = self.parser.parse_field_input(raw_input)
            if err is None:
                # Assign field to simulation
                self.simulation.field = Field(width=res[0], height=res[1])
                print(
                    f"You have created a field of {self.simulation.field.width} x {self.simulation.field.height}."
                )
                return
            print(err)

    def _select_next_command(self) -> int:
        while True:
            print("Please choose from the following options:")
            print("[1] Add a car to field")
            print("[2] Run simulation")
            raw_input: str = input()
            command, err = self.parser.parse_next_command(raw_input)
            if err is None:
                return command
            print(err)

    def _get_car_name(self) -> str:
        while True:
            print("Please enter the name of the car:")
            raw_input: str = input()

            car_names = {c.name for c in self.simulation.cars}
            res, err = self.parser.parse_car_name(raw_input, car_names)
            if err is None:
                return res
            print(err)

    def _get_init_position(self, car_name: str) -> [Position, DirectionEnum]:
        while True:
            print(
                f"Please enter initial position of car {car_name} in x y Direction format:"
            )
            raw_input: str = input()

            init_positions = {str(c.position) for c in self.simulation.cars}
            res, err = self.parser.parse_initial_position(
                raw_input,
                self.simulation.field.width,
                self.simulation.field.height,
                init_positions,
            )
            if err is None:
                return res
            print(err)

    def _get_car_commands(self, car_name) -> list[CommandEnum]:
        while True:
            print(f"Please enter the commands for car {car_name}:")
            raw_input: str = input()
            res, err = self.parser.parse_car_commands(raw_input)
            if err is None:
                return res
            print(err)

    def _get_post_simulation_command(self) -> int:
        while True:
            print("Please choose from the following options:")
            print("[1] Start over")
            print("[2] Exit")
            raw_input: str = input()
            res, err = self.parser.parse_post_simulation_command(raw_input)
            if err is None:
                return res
            print(err)

    def _add_car_to_simulation(self):
        car_name = self._get_car_name()
        pos = self._get_init_position(car_name)
        car_commands = self._get_car_commands(car_name)

        self.simulation.cars.append(
            Car(
                name=car_name,
                position=pos[0],
                facing=pos[1],
                commands=car_commands,
            )
        )

        self._display_current_cars()

    def _run_main_menu(self):
        while True:
            command = self._select_next_command()
            if command == 1:
                self._add_car_to_simulation()
            elif command == 2:
                if not self.simulation.cars:
                    print("You haven't added any cars yet. Please add a car first.")
                    continue
                break

    def _display_current_cars(self):
        print("Your current list of cars are:")
        for car in self.simulation.cars:
            print(
                "- {car_name}, {car_details}, {car_commands}".format(
                    car_name=car.name,
                    car_details=str(car),
                    car_commands="".join(car.commands),
                )
            )

    def _run_simulation(self):
        print("Running simulation...")
        self.simulation.run_simulation()
        print("Simulation finished running...")

    def _display_simulation_results(self):
        print("After simulation your status of current list of cars are:")

        if self.simulation.car_collision_list and self.simulation.car_collision_list:
            # Iterate through different steps to get the list of cars involved in collisions at each step
            for step in self.simulation.car_collision_list.keys():
                for car in self.simulation.car_collision_list[step]:
                    for other_car in [
                        c
                        for c in self.simulation.car_collision_list[step]
                        if c.name != car.name
                    ]:
                        print(
                            f"{car.name} collides with {other_car.name} at {car.position} at step {step}"
                        )

        for car in [c for c in self.simulation.cars if not c.is_collision]:
            print(f"{car.name}, {car.position} {car.facing}")

    def run(self):
        print("Welcome to Auto Driving Car Simulation!")

        while True:
            # Initialize field
            self._get_field()

            # Run main menu
            self._run_main_menu()

            # Run the simulation
            self._run_simulation()
            self._display_simulation_results()

            # Post-simulation command handling
            post_simulation_command = self._get_post_simulation_command()
            if post_simulation_command == 1:
                self.simulation.clear()
            if post_simulation_command == 2:
                break

        print("Thank you for running the simulation. Goodbye!")


def run():
    simulation = CarSimulation()
    simulation.run()


if __name__ == "__main__":
    run()
