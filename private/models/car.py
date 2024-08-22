from private.constants.constants import VERY_LARGE_NUMBER, CommandEnum, DirectionEnum
from private.models.position import Position


class Car:
    def __init__(
        self,
        name: str,
        commands: list[CommandEnum] = [],
        position: Position = Position(0, 0),
        facing: DirectionEnum = DirectionEnum.N,
    ):
        self.name = name
        self.commands = commands
        self.position = position
        self.facing = facing
        self.is_collision: bool = False

    def __str__(self):
        return f"{self.position} {self.facing}"

    def run_command(self, command: CommandEnum | None):
        position = self.position

        if command == CommandEnum.L:
            self._turn_left()
        elif command == CommandEnum.R:
            self._turn_right()
        elif command == CommandEnum.F:
            position = self._move_forward()

        return position

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

    def _move_forward(self) -> Position:
        if self.facing == DirectionEnum.N:
            return Position(self.position.x, self.position.y + 1)
        elif self.facing == DirectionEnum.E:
            return Position(self.position.x + 1, self.position.y)
        elif self.facing == DirectionEnum.S:
            return Position(self.position.x, self.position.y - 1)
        elif self.facing == DirectionEnum.W:
            return Position(self.position.x - 1, self.position.y)
