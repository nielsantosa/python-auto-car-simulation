from private.constants import io_strings
from private.constants.constants import CommandEnum, DirectionEnum
from private.logics.input_parser import InputParser
from private.models.car import Car
from private.models.field import Field
from private.models.position import Position


class CarSimulation:
    def __init__(self):
        self.cars: list[Car] = []
        self.car_names = set()
        self.parser: InputParser = InputParser()

    def _get_input(self, text: str) -> str:
        return input(text + "\n")

    def _init_field(self) -> Field:
        while True:
            raw_input: str = self._get_input(io_strings.WELCOME_IO_STRING)
            res, err = self.parser.parse_field_input(raw_input)
            if err is None:
                return Field(width=res[0], height=res[1])
            print(err)

    def _select_next_command(self) -> int:
        while True:
            next_command_raw: str = self._get_input(
                io_strings.SELECT_ADD_CAR_OR_RUN_SIMULATION_IO_STRING
            )
            command, err = self.parser.parse_next_command(next_command_raw)
            if err is None:
                return command
            print(err)

    def _get_car_name(self) -> str:
        while True:
            raw_input: str = self._get_input(io_strings.ENTER_CAR_NAME_IO_STRING)
            res, err = self.parser.parse_car_name(raw_input, self.car_names)
            if err is None:
                return res
            print(err)

    def _get_init_position(
        self, car_name: str, field: Field
    ) -> [int, int, DirectionEnum]:
        while True:
            raw_input: str = self._get_input(
                io_strings.ENTER_INITIAL_POSITION_IO_STRING.format(car_name=car_name)
            )
            res, err = self.parser.parse_initial_position(
                raw_input, field.width, field.height
            )
            if err is None:
                return res
            print(err)

    def _get_car_commands(self, car_name) -> list[CommandEnum]:
        while True:
            raw_input = self._get_input(
                io_strings.ENTER_CAR_COMMANDS_IO_STRING.format(car_name=car_name)
            )
            res, err = self.parser.parse_car_commands(raw_input)
            if err is None:
                return res
            print(err)

    def _get_post_simulation_command(self) -> int:
        while True:
            raw_input = self._get_input(io_strings.SELECT_POST_SIMULATION_COMMAND)
            res, err = self.parser.parse_post_simulation_command(raw_input)
            if err is None:
                return res
            print(err)

    def _add_cars_to_field(self, field: Field):
        while True:
            command = self._select_next_command()
            if command == 2:
                if not self.cars:
                    print("You haven't added any cars yet. Please add a car first.")
                    continue
                break

            car_name = self._get_car_name()
            pos = self._get_init_position(car_name, field)
            car_commands = self._get_car_commands(car_name)

            self.car_names.add(car_name)
            self.cars.append(Car(
                name=car_name,
                position=Position(pos[0], pos[1]),
                facing=pos[2],
                max_x=field.width,
                max_y=field.height,
                commands=car_commands,
            ))

            self._display_current_cars()

    def _display_current_cars(self):
        print(io_strings.SHOW_CURRENT_LIST_OF_CARS_STRING)
        for car in self.cars:
            print(io_strings.SHOW_CAR_DESCRIPTION.format(
                car_name=car.name,
                car_details=str(car),
                car_commands="".join(car.commands),
            ))

    def _run_simulation(self):
        current_pos_dict = {}
        has_collision = False
        collisions_car = []
        collisions_pos = None
        no_step = 0

        while True:
            run_simulation = False
            for car in self.cars:
                # Check for collisions
                car_pos_key = str(car.position)
                if car_pos_key in current_pos_dict:
                    has_collision = True
                    collisions_car = [current_pos_dict[car_pos_key], car.name]
                    collisions_pos = car.position
                    break
                current_pos_dict[car_pos_key] = car.name

                # Process commands
                if car.commands:
                    run_simulation = True
                    com = car.commands.pop(0)
                    car.run_command(com)

            if has_collision:
                break
            if not run_simulation:
                break
            no_step += 1

        return ((collisions_car, collisions_pos), no_step) if has_collision else (None, no_step)

    def _display_simulation_results(self, collisions, no_step):
        print("After simulation, the result is:")
        if collisions:
            car_name_a, car_name_b = collisions[0]
            car_pos = collisions[1]
            print(f"{car_name_a}, collides with {car_name_b} at {car_pos} at step {no_step}")
            print(f"{car_name_b}, collides with {car_name_a} at {car_pos} at step {no_step}")
        else:
            for car in self.cars:
                print(f"- {car.name}, {str(car)}")

    def run(self):
        while True:
            # Initialize field
            field = self._init_field()
            print(
                io_strings.FIELD_CREATED_IO_STRING.format(
                    width=field.width, height=field.height
                )
            )

            # Add cars to the field
            self._add_cars_to_field(field)

            # Run the simulation
            collisions, no_step = self._run_simulation()
            self._display_simulation_results(collisions, no_step)

            # Post-simulation command handling
            post_simulation_command = self._get_post_simulation_command()
            if post_simulation_command == 2:
                print("Thank you for running the simulation. Goodbye!")
                break

            # Reset added cars
            self.cars = []


def run():
    simulation = CarSimulation()
    simulation.run()


if __name__ == "__main__":
    run()
