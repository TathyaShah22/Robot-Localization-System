"""
Belief State Management for Robot Localization
Handles the set of possible locations for the robot.
"""

from typing import Set, Tuple, List

def get_initial_belief_state(ship: List[List[str]]) -> Set[Tuple[int, int]]:
    """
    Returns the initial belief state, which is the set of all open cells.

    Args:
        ship: The 2D list representing the ship layout.

    Returns:
        A set of (row, col) tuples for all open cells.
    """
    open_cells = set()
    for r, row in enumerate(ship):
        for c, cell in enumerate(row):
            if cell == 'open':
                open_cells.add((r, c))
    return open_cells

def update_belief_state(current_state: Set[Tuple[int, int]], move: str, ship: List[List[str]]) -> Set[Tuple[int, int]]:
    """
    Updates the belief state based on a single move.

    Args:
        current_state: A set of (row, col) tuples representing possible locations.
        move: The move to attempt ('up', 'down', 'left', 'right').
        ship: The 2D list representing the ship layout.

    Returns:
        A new set of possible locations after the move.
    """
    new_state = set()
    D = len(ship)
    
    move_map = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }
    
    if move not in move_map:
        raise ValueError(f"Invalid move: {move}. Must be one of {list(move_map.keys())}")
    
    dr, dc = move_map[move]
    
    for r, c in current_state:
        nr, nc = r + dr, c + dc
        
        # Check if the new position is valid and open
        if 0 <= nr < D and 0 <= nc < D and ship[nr][nc] == 'open':
            new_state.add((nr, nc))
        else:
            # If the move is invalid (hits a wall or goes off the grid), the bot stays in place
            new_state.add((r, c))
            
    return new_state