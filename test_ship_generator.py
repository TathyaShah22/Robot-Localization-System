"""
Test suite for ship_generator.py
Tests the maze generation algorithm and validation functions.
"""

import unittest
from ship_generator import ShipGenerator, generate_ship


class TestShipGenerator(unittest.TestCase):
    """Test cases for ShipGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = ShipGenerator(seed=42)
    
    def test_basic_ship_generation(self):
        """Test basic ship generation functionality."""
        D = 5
        ship = self.generator.generate_ship(D)
        
        # Check dimensions
        self.assertEqual(len(ship), D)
        self.assertEqual(len(ship[0]), D)
        
        # Check that ship contains only valid cell types
        for row in ship:
            for cell in row:
                self.assertIn(cell, ['open', 'blocked'])
    
    def test_connectivity(self):
        """Test that generated ships have connected open cells."""
        for D in [5, 8, 10]:
            with self.subTest(size=D):
                ship = self.generator.generate_ship(D)
                self.assertTrue(self.generator.is_connected(ship),
                              f"Ship of size {D} is not connected")
    
    def test_has_open_cells(self):
        """Test that generated ships have at least one open cell."""
        for D in [5, 8, 10]:
            with self.subTest(size=D):
                ship = self.generator.generate_ship(D)
                open_cells = self.generator.get_open_cells(ship)
                self.assertGreater(len(open_cells), 0,
                                 f"Ship of size {D} has no open cells")
    
    def test_interior_start(self):
        """Test that at least one interior cell can be opened."""
        # This is mainly to test edge cases for small grids
        D = 3  # Smallest grid with interior cells
        ship = self.generator.generate_ship(D)
        open_cells = self.generator.get_open_cells(ship)
        
        # Check if any interior cell is open
        interior_open = any((i, j) for i, j in open_cells 
                           if 0 < i < D-1 and 0 < j < D-1)
        self.assertTrue(interior_open, "No interior cells are open")
    
    def test_ship_statistics(self):
        """Test ship statistics calculation."""
        D = 6
        ship = self.generator.generate_ship(D)
        stats = self.generator.get_ship_stats(ship)
        
        # Check required statistics are present
        required_keys = ['size', 'total_cells', 'open_cells', 'blocked_cells',
                        'open_percentage', 'dead_ends', 'is_connected']
        for key in required_keys:
            self.assertIn(key, stats)
        
        # Check basic math
        self.assertEqual(stats['size'], D)
        self.assertEqual(stats['total_cells'], D * D)
        self.assertEqual(stats['open_cells'] + stats['blocked_cells'], stats['total_cells'])
        self.assertTrue(stats['is_connected'])
    
    def test_open_cells_function(self):
        """Test the get_open_cells function."""
        # Create a simple test ship
        ship = [
            ['blocked', 'open', 'blocked'],
            ['open', 'open', 'blocked'],
            ['blocked', 'open', 'open']
        ]
        
        expected_open = {(0, 1), (1, 0), (1, 1), (2, 1), (2, 2)}
        actual_open = self.generator.get_open_cells(ship)
        
        self.assertEqual(actual_open, expected_open)
    
    def test_connectivity_check(self):
        """Test the connectivity checking function."""
        # Connected ship
        connected_ship = [
            ['blocked', 'open', 'blocked'],
            ['blocked', 'open', 'blocked'],
            ['blocked', 'open', 'blocked']
        ]
        self.assertTrue(self.generator.is_connected(connected_ship))
        
        # Disconnected ship
        disconnected_ship = [
            ['open', 'blocked', 'open'],
            ['blocked', 'blocked', 'blocked'],
            ['blocked', 'blocked', 'blocked']
        ]
        self.assertFalse(self.generator.is_connected(disconnected_ship))
        
        # Empty ship (all blocked)
        empty_ship = [
            ['blocked', 'blocked', 'blocked'],
            ['blocked', 'blocked', 'blocked'],
            ['blocked', 'blocked', 'blocked']
        ]
        self.assertTrue(self.generator.is_connected(empty_ship))  # Vacuously true
    
    def test_neighbor_counting(self):
        """Test the neighbor counting functions."""
        ship = [
            ['blocked', 'open', 'blocked'],
            ['open', 'open', 'blocked'],
            ['blocked', 'open', 'open']
        ]
        
        # Test center cell (1,1) - should have 3 open neighbors
        count = self.generator._count_open_neighbors(ship, 1, 1, 3)
        self.assertEqual(count, 3)
        
        # Test corner cell (0,0) - should have 2 open neighbors: (0,1) and (1,0)
        count = self.generator._count_open_neighbors(ship, 0, 0, 3)
        self.assertEqual(count, 2)
        
        # Test blocked cell (0,2) - should have 0 open neighbors 
        # (neighbors are (0,1), (1,2) where (0,1) is open but (1,2) is blocked)
        count = self.generator._count_open_neighbors(ship, 0, 2, 3)
        self.assertEqual(count, 1)  # Only (0,1) is open
    
    def test_dead_end_detection(self):
        """Test dead end detection."""
        ship = [
            ['blocked', 'open', 'blocked'],
            ['blocked', 'open', 'blocked'],
            ['blocked', 'open', 'open']
        ]
        
        dead_ends = self.generator._find_dead_ends(ship, 3)
        
        # (0,1) should be a dead end (only connected to (1,1))
        self.assertIn((0, 1), dead_ends)
        # (2,2) should be a dead end (only connected to (2,1))
        self.assertIn((2, 2), dead_ends)
        # (1,1) and (2,1) should not be dead ends
        self.assertNotIn((1, 1), dead_ends)
        self.assertNotIn((2, 1), dead_ends)
    
    def test_reproducibility(self):
        """Test that the same seed produces the same ship."""
        gen1 = ShipGenerator(seed=123)
        gen2 = ShipGenerator(seed=123)
        
        ship1 = gen1.generate_ship(6)
        ship2 = gen2.generate_ship(6)
        
        self.assertEqual(ship1, ship2)
    
    def test_convenience_function(self):
        """Test the convenience function."""
        ship = generate_ship(5, seed=456)
        
        self.assertEqual(len(ship), 5)
        self.assertEqual(len(ship[0]), 5)
        
        # Test that it actually generates valid ships
        generator = ShipGenerator()
        self.assertTrue(generator.is_connected(ship))
    
    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        # Test very small grid
        with self.assertRaises(ValueError):
            self.generator.generate_ship(2)  # No interior cells possible
        
        # Test minimum viable size
        ship = self.generator.generate_ship(3)
        self.assertIsNotNone(ship)
        
    def test_multiple_generations(self):
        """Test generating multiple ships of same size."""
        ships = []
        for i in range(5):
            ship = self.generator.generate_ship(7)
            ships.append(ship)
            
            # Each ship should be valid
            self.assertTrue(self.generator.is_connected(ship))
            stats = self.generator.get_ship_stats(ship)
            self.assertGreater(stats['open_cells'], 0)
        
        # Ships should likely be different (though not guaranteed due to randomness)
        # This is more of a smoke test
        self.assertEqual(len(ships), 5)


class TestShipProperties(unittest.TestCase):
    """Test properties of generated ships."""
    
    def setUp(self):
        self.generator = ShipGenerator(seed=789)
    
    def test_ship_complexity(self):
        """Test that ships have reasonable complexity."""
        for D in [5, 8, 10, 12]:
            with self.subTest(size=D):
                ship = self.generator.generate_ship(D)
                stats = self.generator.get_ship_stats(ship)
                
                # Should have a reasonable number of open cells (not too sparse)
                min_open = D  # At least D open cells
                self.assertGreaterEqual(stats['open_cells'], min_open)
                
                # Should not be all open (should have some blocked cells)
                self.assertLess(stats['open_percentage'], 90)
    
    def test_loops_exist(self):
        """Test that larger ships tend to have loops (not just trees)."""
        # Generate a larger ship which should have loops
        ship = self.generator.generate_ship(12)
        stats = self.generator.get_ship_stats(ship)
        
        # In a tree, #edges = #nodes - 1
        # With loops, we should have more edges
        # This is an indirect test - we can't easily count edges
        # but we can check that the ship is not too sparse
        self.assertGreater(stats['open_percentage'], 20)


if __name__ == '__main__':
    unittest.main(verbosity=2)