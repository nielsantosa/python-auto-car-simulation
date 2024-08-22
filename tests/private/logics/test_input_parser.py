import pytest

from private.constants.constants import CommandEnum, DirectionEnum
from private.models.position import Position
from private.logics.input_parser import InputParser


class TestInputParser:
    @pytest.mark.parametrize(
        "input_raw, expected_result, expected_error",
        [
            ("10 20", (10, 20), None),  # Test valid input
            (
                "10",
                None,
                "Please insert 'x y'. Example: '10 10'",
            ),  # Test too few arguments
            (
                "10 20 30",
                None,
                "Please insert 'x y'. Example: '10 10'",
            ),  # Test too many arguments
            (
                "10 abc",
                None,
                "Please insert numbers 'x y'. Example: '10 10'",
            ),  # Test non-numerical input
            ("", None, "Please insert 'x y'. Example: '10 10'"),  # Test empty string
        ],
    )
    def test_parse_field_input(self, input_raw, expected_result, expected_error):
        parser = InputParser()
        result, error = parser.parse_field_input(input_raw)
        assert result == expected_result
        assert error == expected_error

    @pytest.mark.parametrize(
        "next_command_raw, expected_result, expected_error",
        [
            ("1", 1, None),  # Test valid command 1
            ("3", None, "Please insert command '1' or '2'"),  # Test invalid command
            (
                "abc",
                None,
                "Please insert command '1' or '2'",
            ),  # Test non-numerical input
            ("", None, "Please insert command '1' or '2'"),  # Test empty string
        ],
    )
    def test_parse_next_command(
        self, next_command_raw, expected_result, expected_error
    ):
        parser = InputParser()
        result, error = parser.parse_next_command(next_command_raw)
        assert result == expected_result
        assert error == expected_error

    @pytest.mark.parametrize(
        "raw_str, car_names, expected_result, expected_error",
        [
            ("Toyota", {"Honda", "Ford"}, "Toyota", None),  # Test valid unique car name
            ("", {"Honda", "Ford"}, None, "Name cannot be blank"),  # Test empty name
            (
                "Honda",
                {"Honda", "Ford"},
                None,
                "Name exist already. Please choose other name",
            ),  # Test name already exists
            (
                "Chevrolet",
                {"Ford", "Honda"},
                "Chevrolet",
                None,
            ),  # Test another valid unique car name
        ],
    )
    def test_parse_car_name(self, raw_str, car_names, expected_result, expected_error):
        parser = InputParser()
        result, error = parser.parse_car_name(raw_str, car_names)
        assert result == expected_result
        assert error == expected_error

    @pytest.mark.parametrize(
        "raw_str, width, height, expected_result, expected_error",
        [
            ("1 2 N", 5, 5, (Position(1, 2), DirectionEnum.N), None),  # Test valid input
            (
                "1 2",
                5,
                5,
                None,
                "Please enter initial position of car A in x y Direction. Example: '1 2 N'",
            ),  # Missing direction
            (
                "1 2 N E",
                5,
                5,
                None,
                "Please enter initial position of car A in x y Direction. Example: '1 2 N'",
            ),  # Too many arguments
            (
                "-1 2 N",
                5,
                5,
                None,
                "x must be gte 0 or lt field's width",
            ),  # Invalid x coordinate
            (
                "2 5 N",
                5,
                5,
                None,
                "y must be gte 0 or lt field's height",
            ),  # Invalid y coordinate
            (
                "1 2 A",
                5,
                5,
                None,
                "Direction should be 'N', 'E', 'S', 'W' only",
            ),  # Invalid direction
        ],
    )
    def test_parse_initial_position(
        self, raw_str, width, height, expected_result, expected_error
    ):
        parser = InputParser()
        initial_positions: set[str] = set()
        result, error = parser.parse_initial_position(raw_str, width, height, initial_positions)
        assert result == expected_result
        assert error == expected_error

    @pytest.mark.parametrize(
        "raw_str, expected_result, expected_error",
        [
            (
                "FLLFR",
                [
                    CommandEnum.F,
                    CommandEnum.L,
                    CommandEnum.L,
                    CommandEnum.F,
                    CommandEnum.R,
                ],
                None,
            ),  # Mixed commands
            ("", [], None),  # Test empty string
            (
                "FGH12",
                None,
                "Characters should be 'F' 'L' or 'R' only",
            ),  # Invalid commands
        ],
    )
    def test_parse_car_commands(self, raw_str, expected_result, expected_error):
        parser = InputParser()
        result, error = parser.parse_car_commands(raw_str)
        assert result == expected_result
        assert error == expected_error

    @pytest.mark.parametrize(
        "raw_str, expected_result, expected_error",
        [
            ("1", 1, None),  # Valid command '1'
            ("3", None, "Please insert command '1' or '2'"),  # Invalid command
            ("abc", None, "Please insert command '1' or '2'"),  # Non-numeric input
            ("", None, "Please insert command '1' or '2'"),  # Empty input
            (None, None, "Please insert command '1' or '2'"),  # None input
            ("1.5", None, "Please insert command '1' or '2'"),  # Float input
        ],
    )
    def test_parse_post_simulation_command(
        self, raw_str, expected_result, expected_error
    ):
        parser = InputParser()
        result, error = parser.parse_post_simulation_command(raw_str)
        assert result == expected_result
        assert error == expected_error
