from typing import TypeAlias
from private.constants import io_strings


error: TypeAlias = str | None


DIRECTIONS = {"N", "E", "S", "W"}
COMMANDS = {"L", "R", "F"}
VERY_LARGE_NUMBER = 9999


class Position:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"


class Car:
    def __init__(
            self,
            name: str,
            commands: list[str] = [],
            position: Position = Position(0, 0),
            facing: str = "N",
            max_x: int = VERY_LARGE_NUMBER,
            max_y: int = VERY_LARGE_NUMBER,
        ):
        self.name = name
        self.commands = commands
        self.position = position
        self.facing = facing
        self.max_x = max_x
        self.max_y = max_y

    def __str__(self):
        return f"{self.position} {self.facing}"

    def run_command(self, command):
        command_dict = {
            "L": self._turn_left,
            "R": self._turn_right,
            "F": self._move_forward,
        }
        command_func = command_dict.get(command)
        command_func()

    def _turn_left(self):
        turn_left_dict = {
            "N": "W",
            "E": "N",
            "S": "E",
            "W": "S",
        }
        self.facing = turn_left_dict.get(self.facing)

    def _turn_right(self):
        turn_left_dict = {
            "N": "E",
            "E": "S",
            "S": "W",
            "W": "N",
        }
        self.facing = turn_left_dict.get(self.facing)

    def _move_forward(self):
        if self.facing == "N":
            self.position.y = min(self.position.y + 1, self.max_y)
            return
        if self.facing == "E":
            self.position.x = min(self.position.x + 1, self.max_x)
            return
        if self.facing == "S":
            self.position.y = max(self.position.y - 1, 0)
            return
        if self.facing == "W":
            self.position.x = max(self.position.x - 1, 0)
            return


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height


class InputParser:
    def parse_board_input(self, board_input_raw: str) -> (list[int], error):
        inputs: list[str] = board_input_raw.split(" ")

        # validate
        if len(inputs) != 2:
            return [], "Please insert 'x y'. Example: '10 10'"

        try:
            width = int(inputs[0])
            height = int(inputs[1])
        except Exception as e:
            return [], "Please insert numbers 'x y'. Example: '10 10'"

        return [width, height], None

    def parse_next_command(self, next_command_raw: str) -> (int | None, error):
        # validate
        try:
            command_num = int(next_command_raw)
        except Exception as e:
            return None, "Please insert command '1' or '2'"

        if command_num not in {1, 2}:
            return None, "Please insert command '1' or '2'"

        return command_num, None

    def parse_car_name(self, car_name_raw: str, car_names: set) -> (str | None, error):
        if car_name_raw in car_names:
            return None, "Name exist already. Please choose other name"
        # validate
        return car_name_raw, None

    def parse_initial_position(self, raw_str: str, width: int, height: int) -> (list[str], error):
        # validate
        inputs: list[str] = raw_str.split(" ")
        if len(inputs) != 3:
            return None, "Please enter initial position of car A in x y Direction format:"

        try:
            x: int = int(inputs[0])
            y: int = int(inputs[1])
            dir: string = inputs[2]
            if x < 0 or x >= width:
                return None, "x must be gte than 0 or less than width"
            if y < 0 or y >= height:
                return None, "y must be gte than 0 less than height"
            if dir not in DIRECTIONS:
                return None, "Direction should be 'N', 'E', 'S', 'W' only"
        except Exception as e:
            return None, "Please enter initial position of car A in x y Direction format:"

        return [x, y, dir], None

    def parse_car_commands(self, raw_str: str) -> (list[str], error):
        commands = []
        for c in raw_str:
            if c not in COMMANDS:
                return None, "Characters should be 'F' 'L' or 'R' only"
            commands.append(c)

        return commands, None

    def parse_post_simulation_command(self, raw_str: str) -> (list[str], error):
        # validate
        try:
            command_num = int(raw_str)
        except Exception as e:
            return None, "Please insert command '1' or '2'"

        if command_num not in {1, 2}:
            return None, "Please insert command '1' or '2'"

        return command_num, None


class Play:
    def __init__(self):
        self.cars: list[Car] = []
        self.car_names = set()
        self.parser: InputParser = InputParser()

    def _get_input(self, text: str) -> str:
        return input(text + "\n")

    def _init_board(self) -> Board:
        err: str = "something"
        while True:
            board_input_raw: str = self._get_input(io_strings.WELCOME_IO_STRING)
            board_input, err = self.parser.parse_board_input(board_input_raw)
            if err is None:
                return Board(width=board_input[0], height=board_input[1])
            print(err)

    def _select_next_command(self) -> int:
        while True:
            next_command_raw: str = self._get_input(io_strings.SELECT_ADD_CAR_OR_RUN_SIMULATION_IO_STRING)
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

    def _get_init_position(self, car_name: str, board: Board) -> [int, int, str]:
        while True:
            raw_input: str = self._get_input(io_strings.ENTER_INITIAL_POSITION_IO_STRING.format(car_name=car_name))
            res, err = self.parser.parse_initial_position(raw_input, board.width, board.height)
            if err is None:
                return res
            print(err)

    def _get_car_commands(self, car_name) -> list[str]:
        while True:
            raw_input = self._get_input(io_strings.ENTER_CAR_COMMANDS_IO_STRING.format(car_name=car_name))
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

    def run(self):
        while True:
            # initiate board
            board = self._init_board()
            print(io_strings.FIELD_CREATED_IO_STRING.format(width=board.width, height=board.height))

            # while add car
            add_car: bool = True
            while add_car:
                command = self._select_next_command()
                if command == 2:
                    if len(self.cars) == 0:
                        print("You haven't added any car yet. Please add a car first.")
                        continue
                    break

                car_name = self._get_car_name()
                pos = self._get_init_position(car_name, board)
                car_commands = self._get_car_commands(car_name)

                self.car_names.add(car_name)
                self.cars.append(
                    Car(
                        name=car_name,
                        position=Position(pos[0], pos[1]),
                        facing=pos[2],
                        max_x=board.width,
                        max_y=board.height,
                        commands=car_commands,
                    )
                )

                print(io_strings.SHOW_CURRENT_LIST_OF_CARS_STRING)
                for car in self.cars:
                    print(io_strings.SHOW_CAR_DESCRIPTION.format(
                        car_name=car.name,
                        car_details=str(car),
                        car_commands="".join(car.commands),
                    ))

            # run simulation
            run_simulation: bool = True
            has_collision = False
            collisions_car = []
            collisions_pos = None
            no_step = 0
            while run_simulation:
                run_simulation = False
                current_pos_dict: dict = {}
                for car in self.cars:
                    # check position first
                    car_pos_key = str(car.position)
                    if car_pos_key in current_pos_dict:
                        has_collision = True
                        collisions_car = [current_pos_dict[car_pos_key], car.name]
                        collisions_pos = car.position
                        break
                    current_pos_dict[car_pos_key] = car.name

                    # check if car still have commands
                    if len(car.commands) == 0:
                        continue

                    # at least 1 car running, still run simulation
                    run_simulation = True
                    com = car.commands.pop(0)
                    car.run_command(com)

                if has_collision:
                    run_simulation = False
                    break
                no_step += 1

            print("After simulation, the result is:")
            if has_collision:
                print("{car_name_a}, collides with {car_name_b} at {car_pos} at step {no_step}".format(
                    car_name_a = collisions_car[0],
                    car_name_b = collisions_car[1],
                    car_pos = collisions_pos,
                    no_step = no_step
                ))
                print("{car_name_b}, collides with {car_name_a} at {car_pos} at step {no_step}".format(
                    car_name_a = collisions_car[0],
                    car_name_b = collisions_car[1],
                    car_pos = collisions_pos,
                    no_step = no_step
                ))
            else:
                for car in self.cars:
                    print("- {car_name}, {car_position}".format(
                        car_name = car.name,
                        car_position = str(car),
                    ))

            post_simulation_command = self._get_post_simulation_command()
            if post_simulation_command == 2:
                print("Thank you for running the simulation. Goodbye!")
                break

            # clean cars
            self.cars = []

def run():
    game = Play()
    game.run()


if __name__ == "__main__":
    run()
