# Nebulist Robot Localization System

## Project Overview
This project addresses the "kidnapped robot" problem within a constrained environment. A space-faring bot, having lost its sensors and internal orientation due to cosmic radiation, must localize itself within the salvage vessel *Nebulist*.

Given a known map of the ship, the objective is to determine a single, definitive position through a calculated sequence of attempted cardinal moves. Since the bot cannot sense the success or failure of a move (e.g., hitting a wall vs. entering a hallway), it must perform **belief-space planning** to reduce the set of all possible locations to a single coordinate.

## Project Structure
- `ship_generator.py`: Generates grid-based ship layouts using a randomized maze algorithm that ensures connectivity while introducing loops.
- `belief_state.py`: Manages the set of all possible `(row, col)` locations where the bot might be.
- `strategies.py`: Implements three distinct localization approaches:
  - **Baseline (Dr. Cowan's)**: Uses A* pathfinding to reach dead-ends.
  - **Optimality**: Uses Breadth-First Search (BFS) in belief space to find the shortest possible sequence.
  - **Efficiency**: Uses greedy heuristics to reduce the belief set size as quickly as possible.
- `analysis.py`: Runs comparative benchmarks across ship sizes, generating performance metrics and visualizations.
- `main.py`: Entry point for demonstrating the localization strategies.

## Getting Started

### Prerequisites
- Python 3.10+
- `numpy`
- `matplotlib`

### Installation
1. Clone the repository:
```bash
   git clone https://github.com/your-username/nebulist-localization.git
   cd nebulist-localization
```
2. Install dependencies:
```bash
   pip install -r requirements.txt
```

### Running the Analysis
To generate the performance comparison graphs and analyze strategy efficiency, run:
```bash
python analysis.py
```
This will generate `analysis.png`, containing the move count and computation time comparisons.

### Running Tests
We maintain comprehensive unit tests to ensure the integrity of the maze generation and belief state logic:
```bash
python -m unittest discover
```

## Strategy Design
- **Optimality**: Operates by treating each "belief state" (a set of possible locations) as a node in a graph. BFS is used to guarantee the shortest sequence.
- **Efficiency**: Prioritizes computational speed by selecting the move that results in the maximum reduction of the set of possible locations (greedy approach), allowing it to handle much larger ship sizes than the optimal strategy.

## Contributing
This project was developed for CS 520 (Fall 2025). Contributions to the heuristic models or further analysis of worst-case scenarios are welcome.
