# Architecture

- Refer to README.md for main README file
- Refer to README_brief.md for the Assignment Problem.

## Solution Background
On top of adhering to the assignment requirements, my approach for the problem consists of 2 parts:
- Code Organization     - Having a foldering system that have clear separation of concern
- Clean Code            - Having a readable, clean code


## Code Organization
### Foldering System
```
├── .*                          - Dot files for various linting / git settings
├── ARCHITECTURE.md             - Architecture doc for this application
├── README.md                   - Main readme files
├── README_brief.md             - Doc for assignment problems
├── conf                        - Stores all application config and settings
│   ├── requirements.txt
│   ├── requirements_lint.txt
│   └── requirements_test.txt
├── main.py
├── private                     - Encapsulates all application related code. Should not be accessed by external code
│   ├── __init__.py
│   ├── car_simulation.py       - Main Application
│   ├── constants               - Stores all Constants and Enums
│   │   ├── __init__.py
│   │   └── constants.py
│   ├── lib                     - Stores Common helper module
│   │   ├── __init__.py
│   │   ├── error.py
│   │   └── io_read_write.py
│   ├── logics                  - Stores Business Specific Logic (Similar to Service)
│   │   ├── __init__.py
│   │   ├── car_simulation.py
│   │   └── input_parser.py
│   └── models                  - Stores all models
│       ├── __init__.py
│       ├── car.py
│       ├── field.py
│       └── position.py
└── tests                       - Stores all Test Cases - Foldering system mirrors the repo folders
    ├── __init__.py
    └── private
        ├── __init__.py
        ├── logics
        │   ├── __init__.py
        │   ├── test_*.py
        ├── models
        │   ├── __init__.py
        │   └── test_*.py
        └── test_*.py
```

## Clean Code
### Type Hints
Python is a dynamically typed language, and based on my experience, a lot of bugs are due to TypeError.\
By leveraging Type Hints, variables' type are clear.\
Code readability is improved and the code will be less prone to bugs.

### Linter and Formatter
Using linter and formatter helps the developer to achieve the best formatting practice.\
It improves readability and consistency throughout the code.
