"""
Manages the belief state for the Robot Localization project.

The belief state is the set of all possible locations the robot could be in.
This module provides functions to initialize and update this state.
"""

from typing import Set, Tuple, List

def get_initial_belief_state(ship: List[List[str]]) -> Set[Tuple[int, int]]:
    """
    Returns the initial belief state, which is the set of all open cells.

    Args:
        ship: The DxD ship layout.

    Returns:
        A set of (row, col) tuples for all 'open' cells.
    """
    open_cells = set()
    D = len(ship)
    for r in range(D):
        for c in range(D):
            if ship[r][c] == 'open':
                open_cells.add((r, c))
    return open_cells

def update_belief_state(current_locations: Set[Tuple[int, int]], move: str, ship: List[List[str]]) -> Set[Tuple[int, int]]:
    """
    Calculates the new set of possible locations after one attempted move.

    Args:
        current_locations: A set of (row, col) tuples for the current belief state.
        move: The attempted move ('up', 'down', 'left', 'right').
        ship: The DxD ship layout.

    Returns:
        The new set of (row, col) tuples after the move.
    """
    new_locations = set()
    D = len(ship)
    
    # Define move offsets
    move_offsets = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }
    
    dr, dc = move_offsets.get(move.lower(), (0, 0))
    if (dr, dc) == (0, 0) and move.lower() not in move_offsets:
        raise ValueError(f"Invalid move: '{move}'. Must be one of {list(move_offsets.keys())}")

    for r, c in current_locations:
        nr, nc = r + dr, c + dc

        # Check for walls or out-of-bounds
        if 0 <= nr < D and 0 <= nc < D and ship[nr][nc] == 'open':
            new_locations.add((nr, nc))  # Move was successful
        else:
            new_locations.add((r, c))  # Bot hit a wall and stayed put
            
    return new_locations
