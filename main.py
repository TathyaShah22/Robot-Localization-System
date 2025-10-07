"""
Main entry point for the Robot Localization project.
"""

from ship_generator import ShipGenerator
from belief_state import get_initial_belief_state, update_belief_state
from strategies import baseline_strategy, optimal_strategy, efficiency_strategy
from analysis import run_analysis

def main():
    """Generate a ship, run the strategies, and print results."""
    ship_generator = ShipGenerator(seed=42)
    ship = ship_generator.generate_ship(D=5)
    
    print("Generated Ship (5x5):")
    ship_generator.print_ship(ship)
    
    initial_belief_state = get_initial_belief_state(ship)
    print(f"Initial number of possible locations: {len(initial_belief_state)}")
    
    # Baseline Strategy
    baseline_sequence = baseline_strategy(ship, seed=42)
    print(f"\nBaseline strategy found a sequence of {len(baseline_sequence)} moves.")

    # Optimal Strategy
    optimal_sequence = optimal_strategy(ship)
    print(f"Optimal strategy found a sequence of {len(optimal_sequence)} moves.")

    # Efficiency Strategy
    efficiency_sequence = efficiency_strategy(ship)
    print(f"Efficiency strategy found a sequence of {len(efficiency_sequence)} moves.")

    # Verify the final belief state for all three
    final_belief_baseline = initial_belief_state
    for move in baseline_sequence:
        final_belief_baseline = update_belief_state(final_belief_baseline, move, ship)
        
    final_belief_optimal = initial_belief_state
    for move in optimal_sequence:
        final_belief_optimal = update_belief_state(final_belief_optimal, move, ship)
        
    final_belief_efficiency = initial_belief_state
    for move in efficiency_sequence:
        final_belief_efficiency = update_belief_state(final_belief_efficiency, move, ship)
        
    print(f"\nBaseline strategy localized to {len(final_belief_baseline)} position(s).")
    print(f"Optimal strategy localized to {len(final_belief_optimal)} position(s).")
    print(f"Efficiency strategy localized to {len(final_belief_efficiency)} position(s).")

if __name__ == "__main__":
    # main()
    run_analysis()
