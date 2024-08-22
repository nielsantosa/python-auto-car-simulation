import pytest
from unittest.mock import patch
from private.car_simulation import CarSimulation
from private.models.position import Position
from private.constants.constants import DirectionEnum, CommandEnum

class TestCarSimulation:

    @patch('builtins.input', side_effect=[
        "5 5", # Insert field
        "1", # Add car
        "Car1", # Car Name
        "0 0 N", # Pos and Direction
        "F", # Commands
        "2", # Run Simulation
        "2" # Exit
    ])
    @patch('builtins.print')
    def test_run_with_one_car(self, mocked_print, mock_input):
        sim = CarSimulation()
        sim.run()  # Run the simulation

        # Check printed output
        mocked_print.assert_any_call("You have created a field of 5 x 5.")
        mocked_print.assert_any_call("Your current list of cars are:")
        mocked_print.assert_any_call("- Car1, (0,0) N, F")
        mocked_print.assert_any_call("After simulation your status of current list of cars are:")
        mocked_print.assert_any_call("Car1, (0,1) N")

    @patch('builtins.input', side_effect=[
        "5 5", # Insert field
        "2", # Try to run simulation but fail
        "1", # Add car
        "Car1", # Car Name
        "0 0 N", # Pos and Direction
        "F", # Commands
        "2", # Run Simulation
        "2" # Exit
    ])
    @patch('builtins.print')
    def test_run_with_fail_attempt_once_add_car(self, mocked_print, mock_input):
        sim = CarSimulation()
        sim.run()  # Run the simulation

        # Check printed output
        mocked_print.assert_any_call("You have created a field of 5 x 5.")
        mocked_print.assert_any_call("You haven't added any cars yet. Please add a car first.")
        mocked_print.assert_any_call("Your current list of cars are:")
        mocked_print.assert_any_call("- Car1, (0,0) N, F")
        mocked_print.assert_any_call("After simulation your status of current list of cars are:")
        mocked_print.assert_any_call("Car1, (0,1) N")

    @patch('builtins.input', side_effect=[
        "10 10", # Insert field
        "1", # Add car
        "Car1", # Car Name
        "0 0 N", # Pos and Direction
        "F", # Commands
        "1", # Add car
        "Car2", # Car Name
        "0 5 S", # Pos and Direction
        "FFFF", # Commands
        "2", # Run Simulation
        "2" # Exit
    ])
    @patch('builtins.print')
    def test_run_with_multiple_cars(self, mocked_print, mock_input):
        sim = CarSimulation()
        sim.run()  # Run the simulation

        # Check printed output
        mocked_print.assert_any_call("You have created a field of 10 x 10.")
        mocked_print.assert_any_call("Your current list of cars are:")
        mocked_print.assert_any_call("- Car1, (0,0) N, F")
        mocked_print.assert_any_call("- Car2, (0,5) S, FFFF")
        mocked_print.assert_any_call("After simulation your status of current list of cars are:")
        mocked_print.assert_any_call("Car1 collides with Car2 at (0,1) at step 4")
        mocked_print.assert_any_call("Car2 collides with Car1 at (0,1) at step 4")
