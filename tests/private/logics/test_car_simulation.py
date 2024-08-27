import pytest

from private.constants.constants import CommandEnum, DirectionEnum
from private.logics.car_simulation import CarSimulationLogic
from private.models.car import Car
from private.models.field import Field
from private.models.position import Position


class TestCarSimulationLogic:
    @pytest.fixture
    def setup_simulation(self):
        # Setting up a field and cars for tests
        field = Field(10, 10)
        car1 = Car(
            name="Car1",
            commands=[CommandEnum.F, CommandEnum.L],
            position=Position(5, 5),
            facing=DirectionEnum.N,
        )
        car2 = Car(
            name="Car2",
            commands=[CommandEnum.F],
            position=Position(5, 4),
            facing=DirectionEnum.N,
        )
        simulation = CarSimulationLogic(field, [car1, car2])
        return simulation, car1, car2

    def test_initialization(self, setup_simulation):
        simulation, car1, car2 = setup_simulation
        assert simulation.field.width == 10
        assert simulation.field.height == 10
        assert len(simulation.cars) == 2

    def test_run_simulation_fail_initialize_car_list_validity(self, setup_simulation):
        simulation, car1, car2 = setup_simulation
        car1.position.y = 4  # similar to car2
        simulation.run_simulation()
        assert car1.is_collision
        assert car2.is_collision
        assert car1.position == Position(5, 4)  # Both collide at (5, 4)

    def test_run_simulation_no_collisions(self, setup_simulation):
        simulation, car1, car2 = setup_simulation
        simulation.run_simulation()
        assert car1.position == Position(5, 6)  # Moves forward
        assert car1.facing == DirectionEnum.W  # Turns left
        assert car2.position == Position(5, 5)  # Moves forward

    def test_run_simulation_with_collisions(self, setup_simulation):
        # Adjust commands to cause a collision
        simulation, car1, car2 = setup_simulation
        car2.position.x = 6
        car2.position.y = 6
        car2.facing = DirectionEnum.W
        car1.commands = [CommandEnum.F]  # Will go to (5, 6)
        car2.commands = [CommandEnum.F]  # Will also go to (5, 6)

        simulation.run_simulation()
        assert car1.is_collision
        assert car2.is_collision
        assert car1.position == Position(5, 6)  # Both collide at (5, 6)

    def test_out_of_bounds(self):
        field = Field(10, 10)
        car = Car(
            name="Car1", position=Position(0, 0), commands=[], facing=DirectionEnum.N
        )  # Invalid move
        simulation = CarSimulationLogic(field, [car])
        collision_status = simulation.is_colliding_out_of_bound(1, car, Position(-1, 0))
        assert collision_status

    def test_within_bounds(self):
        field = Field(10, 10)
        simulation = CarSimulationLogic(field)
        assert simulation.is_within_bounds(Position(5, 5)) is True
        assert simulation.is_within_bounds(Position(10, 10)) is False
        assert simulation.is_within_bounds(Position(-1, 0)) is False

    def test_clear(self, setup_simulation):
        simulation, _, _ = setup_simulation
        simulation.clear()
        assert len(simulation.cars) == 0
        assert len(simulation.car_collision_list) == 0
