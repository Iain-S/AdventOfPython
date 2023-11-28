# Advent of Code, in Python

## Setup

- Install Python 3.12.
- Set up a virtual environment and install the project with Poetry.
- Set up pre-commit hooks with `pre-commit install --install-hooks`.
- Install watchman for pyre with `brew install watchman`.

## Layout

- `aopy/` has the solutions
- `tests/` has the unit tests
- `inputs/` has my personalised inputs
- `examples/` has the examples inputs

Within each, `a/` and `b/` have files for 2022 and 2023, respectively. `u/` directories are for utilities or utility tests.

## Use

1. `./template 1` to create files for December 1st.
2. `python -m unittest tests/b/test_day1.py` to run the tests.
3. Copy the examples from the problem description into `examples/b/day1.txt`.
4. Copy the personalised input into `inputs/b/day1.txt`.
5. Once you are happy with your solution(s), run `python -m aopy.b.day1` to get the answer(s).
