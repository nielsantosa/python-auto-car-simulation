# Python Auto Car Simulation

A programming assignment.\
Refer to README_brief.md for the Assignment Details.\
Refer to ARCHITECTURE.md for explanation about the solution of the Assignment and the explanation about this repo Architecture.

## Installation and Requirements
- Python 3.11.1 and above

## Running the program
Make sure you have virtualenv or pyenv installed.\
Setup a virtualenv for this package

Once virtualenv is activated, run this command
```
python main.go
```

## For Development
Tools to help for linting and formatting: pre-commit, flake8, ruff, black, and isort\
How to use:
```
pip install conf/requirements_lint.txt

pre-commit run --all-files
```

## For Testing
Tools used : pytest and pytest-cov\
How to run test:
```
pip install conf/requirements_test.txt

# Setup PYTHONPATH if it doesn't work
export PYTHONPATH=<DIRECTORY_TO_THIS_REPO>

pytest --cov=. tests/
```

### Github Actions
- Enabled Github Actions to simulate a "Deployment" on production level
- Currently, it's only used to run test cases.
- On prod, test failures will not proceed with deployment. So the developer can ensure all test cases are passed before deployment

