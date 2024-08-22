from enum import StrEnum, auto


class UpperStrEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Override auto() to return the name as value
        """
        return name


class DirectionEnum(UpperStrEnum):
    N = auto()
    E = auto()
    S = auto()
    W = auto()


class CommandEnum(UpperStrEnum):
    L = auto()
    R = auto()
    F = auto()
