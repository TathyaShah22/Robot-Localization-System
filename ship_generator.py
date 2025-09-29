"""
Ship Generator for Robot Localization Project
Implements the maze generation algorithm specified in the PDF.
"""

import random
import numpy as np
from typing import List, Tuple, Set
from collections import deque

class ShipGenerator:
    """Generates ship layouts using the specified maze algorithm."""
    
    def __init__(self, seed: int = None):
        """Initialize with optional random seed for reproducibility."""
        self.rng = random.Random(seed) if seed is not None else random
    
    def generate_ship(self, D: int) -> List[List[str]]:
        """
        Generate a D×D ship layout following the PDF algorithm:
        1. Start with all blocked cells
        2. Open one random interior cell
        3. Iteratively open blocked cells with exactly one open neighbor
        4. Add loops by opening ~50% of dead-end neighbors
        
        Args:
            D: Grid dimension (D×D)
            
        Returns:
            2D list where 'open' = passable, 'blocked' = wall
        """
        # Step 1: Start with all blocked cells
        ship = [['blocked' for _ in range(D)] for _ in range(D)]
        
        # Step 2: Choose random interior cell and open it
        interior_cells = [(i, j) for i in range(1, D-1) for j in range(1, D-1)]
        if not interior_cells:
            raise ValueError(f"Grid size {D} too small for interior cells")
        
        start_cell = self.rng.choice(interior_cells)
        ship[start_cell[0]][start_cell[1]] = 'open'
        
        # Step 3: Iteratively open cells with exactly one open neighbor
        while True:
            candidates = self._find_single_neighbor_cells(ship, D)
            if not candidates:
                break
            
            # Pick random candidate and open it
            chosen = self.rng.choice(candidates)
            ship[chosen[0]][chosen[1]] = 'open'
        
        # Step 4: Add loops by opening ~50% of dead-end neighbors
        self._add_loops(ship, D)
        
        return ship
    
    def _find_single_neighbor_cells(self, ship: List[List[str]], D: int) -> List[Tuple[int, int]]:
        """Find all blocked cells with exactly one open neighbor."""
        candidates = []
        
        for i in range(D):
            for j in range(D):
                if ship[i][j] == 'blocked':
                    open_neighbors = self._count_open_neighbors(ship, i, j, D)
                    if open_neighbors == 1:
                        candidates.append((i, j))
        
        return candidates
    
    def _count_open_neighbors(self, ship: List[List[str]], i: int, j: int, D: int) -> int:
        """Count open neighbors of cell (i,j)."""
        count = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < D and 0 <= nj < D and ship[ni][nj] == 'open':
                count += 1
        
        return count
    
    def _find_dead_ends(self, ship: List[List[str]], D: int) -> List[Tuple[int, int]]:
        """Find all open cells with exactly one open neighbor (dead ends)."""
        dead_ends = []
        
        for i in range(D):
            for j in range(D):
                if ship[i][j] == 'open':
                    open_neighbors = self._count_open_neighbors(ship, i, j, D)
                    if open_neighbors == 1:
                        dead_ends.append((i, j))
        
        return dead_ends
    
    def _get_blocked_neighbors(self, ship: List[List[str]], i: int, j: int, D: int) -> List[Tuple[int, int]]:
        """Get all blocked neighbors of cell (i,j)."""
        blocked_neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < D and 0 <= nj < D and ship[ni][nj] == 'blocked':
                blocked_neighbors.append((ni, nj))
        
        return blocked_neighbors
    
    def _add_loops(self, ship: List[List[str]], D: int) -> None:
        """Add loops by opening approximately half of dead-end neighbors."""
        dead_ends = self._find_dead_ends(ship, D)
        
        # For each dead end, consider opening one of its blocked neighbors
        for dead_end in dead_ends:
            blocked_neighbors = self._get_blocked_neighbors(ship, dead_end[0], dead_end[1], D)
            
            if blocked_neighbors and self.rng.random() < 0.5:  # ~50% chance
                chosen_neighbor = self.rng.choice(blocked_neighbors)
                ship[chosen_neighbor[0]][chosen_neighbor[1]] = 'open'
    
    def get_open_cells(self, ship: List[List[str]]) -> Set[Tuple[int, int]]:
        """Get set of all open cell coordinates."""
        open_cells = set()
        D = len(ship)
        
        for i in range(D):
            for j in range(D):
                if ship[i][j] == 'open':
                    open_cells.add((i, j))
        
        return open_cells
    
    def is_connected(self, ship: List[List[str]]) -> bool:
        """Verify that all open cells form a connected component using BFS."""
        open_cells = self.get_open_cells(ship)
        if not open_cells:
            return True
        
        # Start BFS from any open cell
        start = next(iter(open_cells))
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        D = len(ship)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while queue:
            i, j = queue.popleft()
            
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if (0 <= ni < D and 0 <= nj < D and 
                    ship[ni][nj] == 'open' and (ni, nj) not in visited):
                    visited.add((ni, nj))
                    queue.append((ni, nj))
        
        return len(visited) == len(open_cells)
    
    def print_ship(self, ship: List[List[str]]) -> None:
        """Print ship layout for visualization."""
        D = len(ship)
        print("Ship Layout:")
        for i in range(D):
            row = ""
            for j in range(D):
                if ship[i][j] == 'open':
                    row += "[ ]"
                else:
                    row += "[#]"
            print(row)
        print()
    
    def get_ship_stats(self, ship: List[List[str]]) -> dict:
        """Get statistics about the generated ship."""
        D = len(ship)
        total_cells = D * D
        open_cells = self.get_open_cells(ship)
        num_open = len(open_cells)
        num_blocked = total_cells - num_open
        
        dead_ends = self._find_dead_ends(ship, D)
        
        return {
            'size': D,
            'total_cells': total_cells,
            'open_cells': num_open,
            'blocked_cells': num_blocked,
            'open_percentage': (num_open / total_cells) * 100,
            'dead_ends': len(dead_ends),
            'is_connected': self.is_connected(ship)
        }


def generate_ship(D: int, seed: int = None) -> List[List[str]]:
    """Convenience function to generate a single ship."""
    generator = ShipGenerator(seed)
    return generator.generate_ship(D)


if __name__ == "__main__":
    # Test the ship generator
    generator = ShipGenerator(seed=42)
    
    # Generate and display a small ship
    ship = generator.generate_ship(8)
    generator.print_ship(ship)
    
    # Print statistics
    stats = generator.get_ship_stats(ship)
    print("Ship Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")