"""
Test suite for belief_state.py
Tests the initialization and updating of the belief state.
"""

import unittest
from belief_state import get_initial_belief_state, update_belief_state

class TestBeliefState(unittest.TestCase):
    """Test cases for belief state management."""

    def setUp(self):
        """Set up a sample ship layout for testing."""
        self.ship = [
            ['open', 'blocked', 'open'],
            ['open', 'open', 'blocked'],
            ['blocked', 'open', 'open']
        ]
        # Open cells are: (0,0), (0,2), (1,0), (1,1), (2,1), (2,2)

    def test_get_initial_belief_state(self):
        """Test that the initial belief state includes all open cells."""
        expected_initial_state = {(0, 0), (0, 2), (1, 0), (1, 1), (2, 1), (2, 2)}
        actual_initial_state = get_initial_belief_state(self.ship)
        self.assertEqual(actual_initial_state, expected_initial_state)

    def test_update_single_successful_move(self):
        """Test a single bot making a successful move."""
        current_state = {(1, 1)}
        # Move 'down' from (1,1) to (2,1) which is open
        new_state = update_belief_state(current_state, 'down', self.ship)
        self.assertEqual(new_state, {(2, 1)})

    def test_update_single_failed_move_wall(self):
        """Test a single bot hitting a wall."""
        current_state = {(1, 1)}
        # Move 'right' from (1,1) to (1,2) which is blocked
        new_state = update_belief_state(current_state, 'right', self.ship)
        self.assertEqual(new_state, {(1, 1)}) # Stays in place

    def test_update_single_failed_move_boundary(self):
        """Test a single bot hitting the edge of the ship."""
        current_state = {(0, 0)}
        # Move 'up' from (0,0) out of bounds
        new_state = update_belief_state(current_state, 'up', self.ship)
        self.assertEqual(new_state, {(0, 0)}) # Stays in place

    def test_update_multiple_bots_mixed_results(self):
        """Test a belief state where some bots move and some hit walls."""
        # (0,0) -> 'right' hits wall at (0,1) -> stays at (0,0)
        # (1,1) -> 'right' hits wall at (1,2) -> stays at (1,1)
        # (2,1) -> 'right' moves to (2,2) -> moves to (2,2)
        current_state = {(0, 0), (1, 1), (2, 1)}
        new_state = update_belief_state(current_state, 'right', self.ship)
        self.assertEqual(new_state, {(0, 0), (1, 1), (2, 2)})

    def test_state_shrinks(self):
        """Test a move that reduces the number of possible locations."""
        # (0,0) -> 'down' moves to (1,0)
        # (1,0) -> 'down' hits wall at (2,0) -> stays at (1,0)
        # After the move, both possible locations are now (1,0)
        current_state = {(0, 0), (1, 0)}
        new_state = update_belief_state(current_state, 'down', self.ship)
        self.assertEqual(new_state, {(1, 0)})
        self.assertEqual(len(new_state), 1)

    def test_all_bots_hit_wall(self):
        """Test a move where all bots in the belief state hit a wall."""
        current_state = {(0, 2), (1, 1)}
        # Move 'up'.
        # (0,2) -> up is out of bounds -> stays at (0,2)
        # (1,1) -> up is (0,1) [blocked] -> stays at (1,1)
        new_state = update_belief_state(current_state, 'up', self.ship)
        self.assertEqual(new_state, {(0, 2), (1, 1)})

    def test_invalid_move_string(self):
        """Test that an invalid move string raises an error."""
        current_state = {(0, 0)}
        with self.assertRaises(ValueError):
            update_belief_state(current_state, 'diagonal', self.ship)

if __name__ == '__main__':
    unittest.main(verbosity=2)
