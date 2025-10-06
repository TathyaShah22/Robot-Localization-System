
import unittest
from main import baseline_strategy
from ship_generator import ShipGenerator

class TestBaselineStrategy(unittest.TestCase):
    def test_baseline_strategy(self):
        # Create a ship generator with a fixed seed for reproducibility
        ship_generator = ShipGenerator(seed=42)
        
        # Generate a ship
        ship = ship_generator.generate_ship(10)
        
        # Run the baseline strategy
        path = baseline_strategy(ship, seed=42)
        
        # Assert that the path is not empty
        self.assertIsNotNone(path)
        
        # Assert that the path is a list of strings
        self.assertIsInstance(path, list)
        self.assertIsInstance(path[0], str)

if __name__ == "__main__":
    unittest.main()
