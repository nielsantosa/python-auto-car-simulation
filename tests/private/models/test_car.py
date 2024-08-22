import pytest

from private.constants.constants import CommandEnum, DirectionEnum
from private.models.car import Car
from private.models.position import Position


# Test cases
@pytest.fixture
def car():
    return Car(name="TestCar")


class TestCar:
    def test_initialization(self, car):
        assert car.name == "TestCar"
        assert car.position.x == 0
        assert car.position.y == 0
        assert car.facing == DirectionEnum.N

    def test_turn_left(self, car):
        car.run_command(CommandEnum.L)
        assert car.facing == DirectionEnum.W
        car.run_command(CommandEnum.L)
        assert car.facing == DirectionEnum.S
        car.run_command(CommandEnum.L)
        assert car.facing == DirectionEnum.E
        car.run_command(CommandEnum.L)
        assert car.facing == DirectionEnum.N

    def test_turn_right(self, car):
        car.run_command(CommandEnum.R)
        assert car.facing == DirectionEnum.E
        car.run_command(CommandEnum.R)
        assert car.facing == DirectionEnum.S
        car.run_command(CommandEnum.R)
        assert car.facing == DirectionEnum.W
        car.run_command(CommandEnum.R)
        assert car.facing == DirectionEnum.N

    def test_move_forward_north(self, car):
        car.run_command(CommandEnum.F)
        assert car.position.y == 1

    def test_move_forward_east(self, car):
        car.facing = DirectionEnum.E
        car.run_command(CommandEnum.F)
        assert car.position.x == 1

    def test_move_forward_south(self, car):
        car.position = Position(0, 1)
        car.facing = DirectionEnum.S
        car.run_command(CommandEnum.F)
        assert car.position.y == 0

    def test_move_forward_west(self, car):
        car.position = Position(1, 0)
        car.facing = DirectionEnum.W
        car.run_command(CommandEnum.F)
        assert car.position.x == 0

    def test_boundaries(self, car):
        car.max_x = 1
        car.max_y = 1
        car.position = Position(1, 1)
        car.facing = DirectionEnum.N
        car.run_command(CommandEnum.F)
        car.run_command(CommandEnum.F)
        assert car.position.y == 1  # Should not go beyond max_y
        car.facing = DirectionEnum.E
        car.run_command(CommandEnum.F)
        assert car.position.x == 1  # Should not go beyond max_x
