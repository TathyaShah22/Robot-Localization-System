import time
import matplotlib.pyplot as plt
from ship_generator import ShipGenerator
from strategies import baseline_strategy, optimal_strategy, efficiency_strategy

def run_analysis():
    """Run the analysis of the three strategies."""
    ship_sizes = [5, 8, 10, 12, 15]
    baseline_moves = []
    optimal_moves = []
    efficiency_moves = []
    
    baseline_times = []
    optimal_times = []
    efficiency_times = []
    
    for size in ship_sizes:
        print(f"Running analysis for ship size: {size}x{size}")
        ship_generator = ShipGenerator(seed=42)
        ship = ship_generator.generate_ship(D=size)
        
        # Baseline Strategy
        start_time = time.time()
        baseline_sequence = baseline_strategy(ship, seed=42)
        baseline_times.append(time.time() - start_time)
        baseline_moves.append(len(baseline_sequence))
        
        # Optimal Strategy
        start_time = time.time()
        optimal_sequence = optimal_strategy(ship)
        optimal_times.append(time.time() - start_time)
        optimal_moves.append(len(optimal_sequence))
        
        # Efficiency Strategy
        start_time = time.time()
        efficiency_sequence = efficiency_strategy(ship)
        efficiency_times.append(time.time() - start_time)
        efficiency_moves.append(len(efficiency_sequence))
        
    # Plotting the results
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(ship_sizes, baseline_moves, marker='o', label='Baseline')
    plt.plot(ship_sizes, optimal_moves, marker='o', label='Optimal')
    plt.plot(ship_sizes, efficiency_moves, marker='o', label='Efficiency')
    plt.xlabel('Ship Size (D)')
    plt.ylabel('Number of Moves')
    plt.title('Number of Moves vs. Ship Size')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(ship_sizes, baseline_times, marker='o', label='Baseline')
    plt.plot(ship_sizes, optimal_times, marker='o', label='Optimal')
    plt.plot(ship_sizes, efficiency_times, marker='o', label='Efficiency')
    plt.xlabel('Ship Size (D)')
    plt.ylabel('Time to Compute (s)')
    plt.title('Time to Compute vs. Ship Size')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('analysis.png')
    print("\nAnalysis complete. Plot saved to analysis.png")

if __name__ == "__main__":
    run_analysis()
