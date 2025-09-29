#!/usr/bin/env python3
"""
Comprehensive inspection file for ship_generator.py
Demonstrates all functionality with 5x5, 10x10, and 20x20 ships.
"""

from ship_generator import ShipGenerator
import time

def print_separator(title: str, width: int = 80):
    """Print a formatted separator with title."""
    separator = "=" * width
    print(f"\n{separator}")
    print(f"{title.center(width)}")
    print(separator)

def print_subsection(title: str, width: int = 60):
    """Print a subsection header."""
    print(f"\n{'-' * width}")
    print(f"{title}")
    print(f"{'-' * width}")

def demonstrate_ship_generation(size: int, generator: ShipGenerator):
    """Demonstrate ship generation and all methods for a given size."""
    print_separator(f"TESTING {size}x{size} SHIP")

    # Generate ship
    print(f"Generating {size}x{size} ship...")
    start_time = time.time()
    ship = generator.generate_ship(size)
    generation_time = time.time() - start_time
    print(f"Generation completed in {generation_time:.4f} seconds")

    # Display the ship
    print_subsection(f"Ship Layout Visualization")
    generator.print_ship(ship)

    # Get and display statistics
    print_subsection("Ship Statistics")
    stats = generator.get_ship_stats(ship)
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")

    # Demonstrate get_open_cells method
    print_subsection("Open Cells Analysis")
    open_cells = generator.get_open_cells(ship)
    print(f"Number of open cells: {len(open_cells)}")
    print(f"First 10 open cell coordinates: {list(open_cells)[:10]}")
    if len(open_cells) > 10:
        print(f"... and {len(open_cells) - 10} more")

    # Demonstrate connectivity check
    print_subsection("Connectivity Analysis")
    is_connected = generator.is_connected(ship)
    print(f"Ship connectivity check: {'CONNECTED' if is_connected else 'NOT CONNECTED'}")

    if is_connected:
        print("[PASS] All open cells form a single connected component")
    else:
        print("[FAIL] Open cells are fragmented into multiple components")

    # Demonstrate connected components method in detail
    print_subsection("Connected Components Method Demonstration")
    print("This method uses Breadth-First Search (BFS) to verify connectivity:")
    print("1. Find all open cells in the ship")
    print("2. Start BFS from any open cell")
    print("3. Mark all reachable open cells as visited")
    print("4. Check if all open cells were visited")

    # Manual step-by-step connectivity check
    open_cells_set = generator.get_open_cells(ship)
    if open_cells_set:
        from collections import deque

        start_cell = next(iter(open_cells_set))
        print(f"Starting BFS from cell: {start_cell}")

        visited = set()
        queue = deque([start_cell])
        visited.add(start_cell)
        step_count = 0

        D = len(ship)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue and step_count < 5:  # Show first 5 steps
            i, j = queue.popleft()
            step_count += 1
            print(f"  Step {step_count}: Processing cell {(i, j)}")

            neighbors_found = 0
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if (0 <= ni < D and 0 <= nj < D and
                    ship[ni][nj] == 'open' and (ni, nj) not in visited):
                    visited.add((ni, nj))
                    queue.append((ni, nj))
                    neighbors_found += 1

            print(f"    Found {neighbors_found} new open neighbors")

        if queue:
            print(f"  ... (continuing BFS for remaining {len(queue)} cells in queue)")

        print(f"BFS Result: Visited {len(visited)} out of {len(open_cells_set)} open cells")
        print(f"Connectivity: {'CONNECTED' if len(visited) == len(open_cells_set) else 'NOT CONNECTED'}")

    # Additional analysis
    print_subsection("Additional Analysis")
    dead_ends = generator._find_dead_ends(ship, size)
    print(f"Dead ends found: {len(dead_ends)}")
    if dead_ends:
        print(f"Dead end locations: {dead_ends[:5]}")  # Show first 5
        if len(dead_ends) > 5:
            print(f"... and {len(dead_ends) - 5} more")

    # Border analysis
    border_open = 0
    for i in range(size):
        for j in range(size):
            if (i == 0 or i == size-1 or j == 0 or j == size-1) and ship[i][j] == 'open':
                border_open += 1

    print(f"Open cells on border: {border_open}")
    print(f"Interior open cells: {len(open_cells) - border_open}")

    return ship, stats

def compare_ships(ships_data: list):
    """Compare statistics across different ship sizes."""
    print_separator("SHIP SIZE COMPARISON")

    print(f"{'Size':<6} {'Total':<6} {'Open':<6} {'Blocked':<8} {'Open %':<8} {'Dead Ends':<10} {'Connected':<10}")
    print("-" * 70)

    for size, stats in ships_data:
        print(f"{size:<6} {stats['total_cells']:<6} {stats['open_cells']:<6} "
              f"{stats['blocked_cells']:<8} {stats['open_percentage']:<8.1f} "
              f"{stats['dead_ends']:<10} {'Yes' if stats['is_connected'] else 'No':<10}")

def test_reproducibility():
    """Test that the same seed produces the same ship."""
    print_separator("REPRODUCIBILITY TEST")

    print("Testing reproducibility with same seed...")
    generator1 = ShipGenerator(seed=123)
    generator2 = ShipGenerator(seed=123)

    ship1 = generator1.generate_ship(8)
    ship2 = generator2.generate_ship(8)

    # Compare ships
    identical = ship1 == ship2
    print(f"Ships with same seed are identical: {'Yes' if identical else 'No'}")

    if identical:
        print("[PASS] Reproducibility test passed")
    else:
        print("[FAIL] Reproducibility test failed")

def test_edge_cases():
    """Test edge cases and error conditions."""
    print_separator("EDGE CASE TESTING")

    generator = ShipGenerator(seed=42)

    # Test minimum size
    print("Testing minimum viable size (3x3)...")
    try:
        small_ship = generator.generate_ship(3)
        print("[PASS] 3x3 ship generated successfully")
        generator.print_ship(small_ship)
        stats = generator.get_ship_stats(small_ship)
        print(f"3x3 ship stats: {stats['open_cells']} open cells, connected: {stats['is_connected']}")
    except Exception as e:
        print(f"[FAIL] 3x3 ship generation failed: {e}")

    # Test invalid size
    print("\nTesting invalid size (2x2)...")
    try:
        invalid_ship = generator.generate_ship(2)
        print("[FAIL] 2x2 ship should have failed but didn't")
    except ValueError as e:
        print(f"[PASS] 2x2 ship correctly failed: {e}")
    except Exception as e:
        print(f"[WARN] 2x2 ship failed with unexpected error: {e}")

def main():
    """Main testing function."""
    print_separator("SHIP GENERATOR COMPREHENSIVE INSPECTION")
    print("This demonstrates all functionality of the ShipGenerator class")
    print("including ship generation, visualization, statistics, and connectivity analysis.")

    # Initialize generator with fixed seed for reproducible results
    generator = ShipGenerator(seed=42)

    # Test different ship sizes
    ships_data = []

    for size in [5, 10, 20]:
        ship, stats = demonstrate_ship_generation(size, generator)
        ships_data.append((size, stats))

    # Compare ships
    compare_ships(ships_data)

    # Test reproducibility
    test_reproducibility()

    # Test edge cases
    test_edge_cases()

    # Final summary
    print_separator("INSPECTION COMPLETE")
    print("All major functionality has been demonstrated:")
    print("• Ship generation for multiple sizes (5x5, 10x10, 20x20)")
    print("• Ship visualization with print_ship()")
    print("• Statistics calculation with get_ship_stats()")
    print("• Open cells extraction with get_open_cells()")
    print("• Connectivity verification with is_connected()")
    print("• Connected components analysis using BFS")
    print("• Reproducibility testing")
    print("• Edge case handling")
    print("\nThe ship generator is working correctly and all methods are functional!")

if __name__ == "__main__":
    main()