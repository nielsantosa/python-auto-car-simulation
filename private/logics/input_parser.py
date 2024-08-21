from private.constants.constants import CommandEnum, DirectionEnum
from private.lib.error import error


class InputParser:
    def parse_field_input(
        self, field_input_raw: str
    ) -> (tuple[int, int] | None, error):
        inputs: list[str] = field_input_raw.split(" ")

        if len(inputs) != 2:
            return None, "Please insert 'x y'. Example: '10 10'"

        try:
            width = int(inputs[0])
            height = int(inputs[1])
        except (ValueError, TypeError):
            return None, "Please insert numbers 'x y'. Example: '10 10'"

        return (width, height), None

    def parse_next_command(self, next_command_raw: str) -> (int | None, error):
        try:
            command_num = int(next_command_raw)
        except (ValueError, TypeError):
            return None, "Please insert command '1' or '2'"

        if command_num not in {1, 2}:
            return None, "Please insert command '1' or '2'"

        return command_num, None

    def parse_car_name(self, raw_str: str, car_names: set[str]) -> (str | None, error):
        if not raw_str:
            return None, "Name cannot be blank"

        if raw_str in car_names:
            return None, "Name exist already. Please choose other name"

        return raw_str, None

    def parse_initial_position(
        self, raw_str: str, width: int, height: int
    ) -> (tuple[int, int, DirectionEnum] | None, error):
        inputs: list[str] = raw_str.split(" ")
        if len(inputs) != 3:
            return (
                None,
                "Please enter initial position of car A in x y Direction. Example: '1 2 N'",
            )

        try:
            x: int = int(inputs[0])
            y: int = int(inputs[1])
            direction: DirectionEnum = DirectionEnum[inputs[2]]
            if not (0 <= x < width):
                return None, "x must be gte 0 or lt field's width"
            if not (0 <= y < height):
                return None, "y must be gte 0 or lt field's height"
        except ValueError:
            return None, "Please enter valid integer for x and y"
        except KeyError:
            return None, "Direction should be 'N', 'E', 'S', 'W' only"

        return (x, y, direction), None

    def parse_car_commands(self, raw_str: str) -> (list[str], error):
        commands: list[str] = []
        for c in raw_str:
            try:
                commands.append(CommandEnum[c])
            except KeyError:
                return None, "Characters should be 'F' 'L' or 'R' only"

        print(commands)
        return commands, None

    def parse_post_simulation_command(self, raw_str: str) -> (int | None, error):
        try:
            command_num: int = int(raw_str)
        except (ValueError, TypeError):
            return None, "Please insert command '1' or '2'"

        if command_num not in {1, 2}:
            return None, "Please insert command '1' or '2'"

        return command_num, None
