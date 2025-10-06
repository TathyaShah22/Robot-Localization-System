"""
Main entry point for the Robot Localization project.
Implements the Baseline Strategy (Dr. Cowan's) for localization.
"""

import random
import heapq
from ship_generator import ShipGenerator
from belief_state import get_initial_belief_state, update_belief_state
from typing import List, Tuple, Set, Optional

def find_dead_ends(ship: List[List[str]]) -> List[Tuple[int, int]]:
    """Find all open cells with exactly one open neighbor (dead ends)."""
    dead_ends = []
    D = len(ship)
    for r in range(D):
        for c in range(D):
            if ship[r][c] == 'open':
                open_neighbors = 0
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < D and 0 <= nc < D and ship[nr][nc] == 'open':
                        open_neighbors += 1
                if open_neighbors == 1:
                    dead_ends.append((r, c))
    return dead_ends

def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Manhattan distance heuristic for A*. """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(ship: List[List[str]], start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[str]]:
    """A* search to find the shortest path from start to goal."""
    D = len(ship)
    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while frontier:
        _, current = heapq.heappop(frontier)
        
        if current == goal:
            break
            
        for dr, dc, move in [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]:
            next_pos = (current[0] + dr, current[1] + dc)
            
            if 0 <= next_pos[0] < D and 0 <= next_pos[1] < D and ship[next_pos[0]][next_pos[1]] == 'open':
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + heuristic(next_pos, goal)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = (current, move)
    else:
        return None # Path not found

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        prev, move = came_from[current]
        path.append(move)
        current = prev
    path.reverse()
    return path

def baseline_strategy(ship: List[List[str]], seed: int = None) -> List[str]:
    """Implements Dr. Cowan's baseline localization strategy."""
    rng = random.Random(seed) if seed is not None else random
    
    belief_state = get_initial_belief_state(ship)
    dead_ends = find_dead_ends(ship)
    if not dead_ends:
        raise ValueError("No dead ends found in the ship.")
        
    target_cell = rng.choice(dead_ends)
    
    sequence_of_moves = []
    
    while len(belief_state) > 1:
        current_pos = rng.choice(list(belief_state))
        
        path = a_star_search(ship, current_pos, target_cell)
        
        if path:
            for move in path:
                belief_state = update_belief_state(belief_state, move, ship)
                sequence_of_moves.append(move)
                if len(belief_state) == 1:
                    break
    
    return sequence_of_moves

def main():
    """Generate a ship, run the baseline strategy, and print results."""
    ship_generator = ShipGenerator(seed=42)
    ship = ship_generator.generate_ship(D=10)
    
    print("Generated Ship (10x10):")
    ship_generator.print_ship(ship)
    
    initial_belief_state = get_initial_belief_state(ship)
    print(f"Initial number of possible locations: {len(initial_belief_state)}")
    
    localization_sequence = baseline_strategy(ship, seed=42)
    
    print(f"\nLocalization sequence found with {len(localization_sequence)} moves:")
    print(localization_sequence)
    
    # Verify the final belief state
    final_belief_state = initial_belief_state
    for move in localization_sequence:
        final_belief_state = update_belief_state(final_belief_state, move, ship)
        
    print(f"\nFinal number of possible locations: {len(final_belief_state)}")
    if len(final_belief_state) == 1:
        print(f"Successfully localized to: {list(final_belief_state)[0]}")
    else:
        print("Failed to localize to a single position.")

if __name__ == "__main__":
    main()