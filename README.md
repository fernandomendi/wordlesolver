# wordlesolver

wordlesolver is a Python package designed to assist in solving the popular Wordle game. It leverages strategies such as entropy calculation and word filtering to determine the best possible guesses and optimize the solving process.

## Features

- **Entropy Calculation**: Calculate the entropy of possible words to determine the most informative guesses.
- **Word Filtering**: Dynamically filter possible words based on feedback from previous guesses.
- **Language Support**: Support for multiple languages, each with an optimized initial guess.
- **Simulation Mode**: Run simulations to determine the effectiveness of different strategies.

## Installation

Clone the repository and install the necessary dependencies using `pip`:

```bash
git clone https://github.com/yourusername/wordlesolver.git
cd wordlesolver
pip install -e .
```

## Usage

### 1. Solving a Wordle Puzzle
You can use the package to find the best guesses based on feedback from the game. Here's an example:

```python
from wordlesolver.theory import best_guess
from wordlesolver.core.variables import Languages

# Initialize language
language = Languages.EN

# Simulate a series of guesses
steps = [
    {"guess": "tares", "answer": "00010"},
    {"guess": "slant", "answer": "01000"},
]

# Get the best next guess
next_guess = best_guess(steps, language)
print(f"Next best guess: {next_guess}")
```

### 2. Running a Simulation
You can simulate a Wordle game by running a Python script fom the root folder:

```bash
python scripts/solver.py ES
```
This command will output the maximum number of possible words remaining after applying the initial guess.

### 3. Running Tests
To ensure everything is functioning as expected, you can run the unit tests:

```python
pytest tests/
```

## Project Structure
```bash
.
├── data/                        # Data files required by the solver
├── scripts/                     # Scripts for running simulations and other tasks
├── wordlesolver/                # Main package code
│   ├── core/                    # Core components, such as exceptions and variables
│   │   ├── common.py            # Common utilities and validation functions
│   │   ├── exceptions.py        # Custom exception and error handling classes
│   │   ├── variables.py         # Custom data types to be used across the package
│   ├── common.py                # Common utilities and functions used in filter.py and theory.py
│   ├── filter.py                # Functions for filtering possible words
│   ├── theory.py                # Functions implementing wordle-solving strategies
├── tests/                       # Unit tests for the package
├── README.md                    # Project documentation
```

## Contributing
Contributions are welcome! If you have ideas or improvements, please open an issue or submit a pull request. Make sure to follow the coding standards and include appropriate tests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Future Plans
- Add support for additional languages.
- Implement more advanced strategies for word selection.
- Improve the efficiency of the entropy calculation.

## Acknowledgements
I have studied a Mathematics degree and in one of the courses we learnt about Information Theory. However, back in 2022, I did not see the possible uses for this field. A couple of weeks after learning about this in class, a new video popped up on my YouTube feed, it was [Solving Wordle using information theory](https://www.youtube.com/watch?v=v68zYyaEmEA) from [3Blue1Brown](https://www.youtube.com/@3blue1brown). This led me to want to learn more on the topic and develop an initial version of this project.

Now, two years later I have reopened my interest for this topic and have decided to develop a well organised package with all necessary code based on Information Theory and Statistics.
