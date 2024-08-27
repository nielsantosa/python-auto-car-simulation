from private.constants.constants import CommandEnum, DirectionEnum
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

    def run_command(self, command: CommandEnum | None, step: int) -> Position:
        position = self.position

        REVERSE_COMMAND_DICT = {
            CommandEnum.L: CommandEnum.R,
            CommandEnum.R: CommandEnum.L,
            CommandEnum.F: CommandEnum.B,
            CommandEnum.B: CommandEnum.F,
        }

        if command == CommandEnum.L:
            self._turn_left()
        elif command == CommandEnum.R:
            self._turn_right()
        elif command == CommandEnum.F:
            position = self._move_forward()
        elif command == CommandEnum.B:
            position = self._move_backward()
        elif command == CommandEnum.U:
            if (step - 2) < 0:
                return position
            prev_command = self.commands[step - 2]
            return self.run_command(REVERSE_COMMAND_DICT[prev_command], step)

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
        """
        Peek the next position without changing the instance's position
        """
        if self.facing == DirectionEnum.N:
            return Position(self.position.x, self.position.y + 1)
        elif self.facing == DirectionEnum.E:
            return Position(self.position.x + 1, self.position.y)
        elif self.facing == DirectionEnum.S:
            return Position(self.position.x, self.position.y - 1)
        elif self.facing == DirectionEnum.W:
            return Position(self.position.x - 1, self.position.y)

    def _move_backward(self) -> Position:
        """
        Peek the next position without changing the instance's position
        """
        if self.facing == DirectionEnum.N:
            return Position(self.position.x, self.position.y - 1)
        elif self.facing == DirectionEnum.E:
            return Position(self.position.x - 1, self.position.y)
        elif self.facing == DirectionEnum.S:
            return Position(self.position.x, self.position.y + 1)
        elif self.facing == DirectionEnum.W:
            return Position(self.position.x + 1, self.position.y)
