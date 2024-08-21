from private.models.position import Position
from private.constants.constants import DirectionEnum, CommandEnum, VERY_LARGE_NUMBER


class Car:
    def __init__(
            self,
            name: str,
            commands: list[CommandEnum] = [],
            position: Position = Position(0, 0),
            facing: DirectionEnum = DirectionEnum.N,
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
            CommandEnum.L: self._turn_left,
            CommandEnum.R: self._turn_right,
            CommandEnum.F: self._move_forward,
        }
        command_func = command_dict.get(command)
        command_func()

    def _turn_left(self):
        turn_left_dict = {
            DirectionEnum.N: DirectionEnum.W,
            DirectionEnum.E: DirectionEnum.N,
            DirectionEnum.S: DirectionEnum.E,
            DirectionEnum.W: DirectionEnum.S,
        }
        self.facing = turn_left_dict[self.facing]

    def _turn_right(self):
        turn_right_dict = {
            DirectionEnum.N: DirectionEnum.E,
            DirectionEnum.E: DirectionEnum.S,
            DirectionEnum.S: DirectionEnum.W,
            DirectionEnum.W: DirectionEnum.N,
        }
        self.facing = turn_right_dict[self.facing]

    def _move_forward(self):
        if self.facing == DirectionEnum.N:
            self.position.y = min(self.position.y + 1, self.max_y)
        elif self.facing == DirectionEnum.E:
            self.position.x = min(self.position.x + 1, self.max_x)
        elif self.facing == DirectionEnum.S:
            self.position.y = max(self.position.y - 1, 0)
        elif self.facing == DirectionEnum.W:
            self.position.x = max(self.position.x - 1, 0)
