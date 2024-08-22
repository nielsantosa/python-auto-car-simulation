# Python Auto Car Simulation

A programming assignment.
Refer to README_brief.md for the Assignment Details.

## Installation and Requirements
- Python 3.11.1 and above

## Running the program
Make sure you have virtualenv or pyenv installed.
Setup a virtualenv for this package

Once virtualenv is activated, run this command
```
python main.go
```

## For Development
Tools to help for linting and formatting: pre-commit, flake8, ruff, black, and isort
How to use:
```
pip install conf/requirements_lint.txt

pre-commit run --all-files
```

## For Testing
Tools used : pytest and pytest-cov
How to run test:
```
pip install conf/requirements_test.txt

# Setup PYTHONPATH if it doesn't work
export PYTHONPATH=<DIRECTORY_TO_THIS_REPO>

pytest --cov=. tests/
```

