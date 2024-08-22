from private.constants.constants import CommandEnum, DirectionEnum
from private.logics.car_simulation import CarSimulationLogic
from private.logics.input_parser import InputParser
from private.models.car import Car
from private.models.field import Field
from private.models.position import Position
from private.lib.io_read_write import IOReadWrite


class CarSimulation:
    def __init__(self):
        self.parser: InputParser = InputParser()
        self.simulation = CarSimulationLogic()
        self.io_rw = IOReadWrite()

    def _get_field(self):
        while True:
            self.io_rw.write_string(
                "Please enter the width and height of the simulation field in x y format:"
            )
            raw_input: str = self.io_rw.read_string()
            res, err = self.parser.parse_field_input(raw_input)
            if err is None:
                # Assign field to simulation
                self.simulation.field = Field(width=res[0], height=res[1])
                self.io_rw.write_string(
                    f"You have created a field of {self.simulation.field.width} x {self.simulation.field.height}."
                )
                return
            self.io_rw.write_string(err)

    def _select_next_command(self) -> int:
        while True:
            self.io_rw.write_string("Please choose from the following options:")
            self.io_rw.write_string("[1] Add a car to field")
            self.io_rw.write_string("[2] Run simulation")
            raw_input: str = self.io_rw.read_string()
            command, err = self.parser.parse_next_command(raw_input)
            if err is None:
                return command
            self.io_rw.write_string(err)

    def _get_car_name(self) -> str:
        while True:
            self.io_rw.write_string("Please enter the name of the car:")
            raw_input: str = self.io_rw.read_string()

            car_names = {c.name for c in self.simulation.cars}
            res, err = self.parser.parse_car_name(raw_input, car_names)
            if err is None:
                return res
            self.io_rw.write_string(err)

    def _get_init_position(self, car_name: str) -> [Position, DirectionEnum]:
        while True:
            self.io_rw.write_string(
                f"Please enter initial position of car {car_name} in x y Direction format:"
            )
            raw_input: str = self.io_rw.read_string()

            init_positions = {str(c.position) for c in self.simulation.cars}
            res, err = self.parser.parse_initial_position(
                raw_input,
                self.simulation.field.width,
                self.simulation.field.height,
                init_positions,
            )
            if err is None:
                return res
            self.io_rw.write_string(err)

    def _get_car_commands(self, car_name) -> list[CommandEnum]:
        while True:
            self.io_rw.write_string(f"Please enter the commands for car {car_name}:")
            raw_input: str = self.io_rw.read_string()
            res, err = self.parser.parse_car_commands(raw_input)
            if err is None:
                return res
            self.io_rw.write_string(err)

    def _get_post_simulation_command(self) -> int:
        while True:
            self.io_rw.write_string("Please choose from the following options:")
            self.io_rw.write_string("[1] Start over")
            self.io_rw.write_string("[2] Exit")
            raw_input: str = self.io_rw.read_string()
            res, err = self.parser.parse_post_simulation_command(raw_input)
            if err is None:
                return res
            self.io_rw.write_string(err)

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
                    self.io_rw.write_string("You haven't added any cars yet. Please add a car first.")
                    continue
                break

    def _display_current_cars(self):
        self.io_rw.write_string("Your current list of cars are:")
        for car in self.simulation.cars:
            self.io_rw.write_string(
                "- {car_name}, {car_details}, {car_commands}".format(
                    car_name=car.name,
                    car_details=str(car),
                    car_commands="".join(car.commands),
                )
            )

    def _run_simulation(self):
        self.io_rw.write_string("Running simulation...")
        self.simulation.run_simulation()
        self.io_rw.write_string("Simulation finished running...")

    def _display_simulation_results(self):
        self.io_rw.write_string("After simulation your status of current list of cars are:")

        if self.simulation.car_collision_list and self.simulation.car_collision_list:
            # Iterate through different steps to get the list of cars involved in collisions at each step
            for step in self.simulation.car_collision_list.keys():
                for car in self.simulation.car_collision_list[step]:
                    for other_car in [
                        c
                        for c in self.simulation.car_collision_list[step]
                        if c.name != car.name
                    ]:
                        self.io_rw.write_string(
                            f"{car.name} collides with {other_car.name} at {car.position} at step {step}"
                        )

        for car in [c for c in self.simulation.cars if not c.is_collision]:
            self.io_rw.write_string(f"{car.name}, {car.position} {car.facing}")

    def _clear_simulation(self):
        self.simulation.clear()

    def run(self):
        self.io_rw.write_string("Welcome to Auto Driving Car Simulation!")

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
            self._clear_simulation()
            if post_simulation_command == 1:
                pass
            if post_simulation_command == 2:
                break

        self.io_rw.write_string("Thank you for running the simulation. Goodbye!")
