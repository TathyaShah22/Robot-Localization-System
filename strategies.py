"""
Implementation of the localization strategies.
"""

import random
import heapq
from collections import deque
from typing import List, Tuple, Optional
from belief_state import get_initial_belief_state, update_belief_state

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
    """Manhattan distance heuristic for A*."""
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

def optimal_strategy(ship: List[List[str]]) -> List[str]:
    """Finds the shortest sequence of moves to localize the bot using BFS."""
    initial_locations = get_initial_belief_state(ship)
    
    # The queue will store tuples of (current_locations_set, path_so_far)
    queue = deque([(initial_locations, [])]) 
    
    # A set to keep track of visited sets of locations to avoid cycles
    visited = {frozenset(initial_locations)}

    while queue:
        current_locs, path = queue.popleft()

        # Goal check
        if len(current_locs) == 1:
            return path # We found the shortest path!

        for move in ['up', 'down', 'left', 'right']:
            next_locs = update_belief_state(current_locs, move, ship)
            
            # Use frozenset because sets are not hashable and can't be in visited
            if frozenset(next_locs) not in visited:
                visited.add(frozenset(next_locs))
                new_path = path + [move]
                queue.append((next_locs, new_path))
    
    return None # Should not happen on a valid ship

def efficiency_strategy(ship: List[List[str]]) -> List[str]:
    """Finds a localization sequence using a greedy heuristic."""
    belief_state = get_initial_belief_state(ship)
    sequence_of_moves = []
    
    while len(belief_state) > 1:
        best_move = None
        min_resulting_size = len(belief_state)
        
        for move in ['up', 'down', 'left', 'right']:
            new_state = update_belief_state(belief_state, move, ship)
            if len(new_state) < min_resulting_size:
                min_resulting_size = len(new_state)
                best_move = move
        
        if best_move:
            belief_state = update_belief_state(belief_state, best_move, ship)
            sequence_of_moves.append(best_move)
        else:
            # If no move reduces the belief state, we might be stuck.
            # This can happen in highly symmetric ships. To handle this,
            # we can fall back to a random move to try and break the symmetry.
            best_move = random.choice(['up', 'down', 'left', 'right'])
            belief_state = update_belief_state(belief_state, best_move, ship)
            sequence_of_moves.append(best_move)
            
    return sequence_of_moves
