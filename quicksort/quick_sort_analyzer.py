import random
import time
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
import os
import sys

class QuickSortAnalyzer:
    """
    This class implements and compares two types of quicksort algorithms:
    1. Randomized Quicksort - picks pivot randomly
    2. Deterministic Quicksort - always picks first element as pivot
    """
    
    def __init__(self):
        self.comparisons = 0
        
    def reset_comparisons(self):
        """Reset the counter that tracks number of comparisons"""
        self.comparisons = 0
    
    def quick_sort_analyzer(self, arr: List[int], low: int = 0, high: int = None) -> List[int]:
        """
        Quicksort algorithm that chooses pivot element randomly
        
        Parameters:
            arr: The list of numbers to sort
            low: Starting position (default is 0)
            high: Ending position (default is last element)
            
        Returns:
            The sorted list
        """
        if high is None:
            high = len(arr) - 1
            
        if low < high:
            # Choose random pivot and split the array
            pivot_position = self._randomized_partition(arr, low, high)
            
            # Sort left and right parts separately
            self.quick_sort_analyzer(arr, low, pivot_position - 1)
            self.quick_sort_analyzer(arr, pivot_position + 1, high)
            
        return arr
    
    def deterministic_quicksort(self, arr: List[int], low: int = 0, high: int = None) -> List[int]:
        """
        Quicksort algorithm that always chooses first element as pivot
        
        Parameters:
            arr: The list of numbers to sort
            low: Starting position (default is 0)
            high: Ending position (default is last element)
            
        Returns:
            The sorted list
        """
        if high is None:
            high = len(arr) - 1
            
        if low < high:
            # Use first element as pivot and split the array
            pivot_position = self._deterministic_partition(arr, low, high)
            
            # Sort left and right parts separately
            self.deterministic_quicksort(arr, low, pivot_position - 1)
            self.deterministic_quicksort(arr, pivot_position + 1, high)
            
        return arr
    
    def _randomized_partition(self, arr: List[int], low: int, high: int) -> int:
        """
        Split array with randomly chosen pivot element
        
        Parameters:
            arr: Array to split
            low: Starting position
            high: Ending position
            
        Returns:
            Final position of pivot element
        """
        # Pick random element between low and high
        random_index = random.randint(low, high)
        
        # Move random element to last position
        arr[random_index], arr[high] = arr[high], arr[random_index]
        
        # Use last element as pivot
        return self._partition(arr, low, high)
    
    def _deterministic_partition(self, arr: List[int], low: int, high: int) -> int:
        """
        Split array using first element as pivot
        
        Parameters:
            arr: Array to split
            low: Starting position
            high: Ending position
            
        Returns:
            Final position of pivot element
        """
        # Move first element to last position to use same splitting method
        arr[low], arr[high] = arr[high], arr[low]
        
        return self._partition(arr, low, high)
    
    def _partition(self, arr: List[int], low: int, high: int) -> int:
        """
        Split array around pivot element (last element)
        All smaller elements go to left, larger elements go to right
        
        Parameters:
            arr: Array to split
            low: Starting position
            high: Ending position (where pivot is located)
            
        Returns:
            Final position of pivot element
        """
        pivot = arr[high]  # Last element is our pivot
        i = low - 1  # Position for smaller elements
        
        for j in range(low, high):
            self.comparisons += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def generate_test_arrays(self, size: int) -> dict:
        """
        Create different types of test arrays for comparison
        
        Parameters:
            size: How many elements in each array
            
        Returns:
            Dictionary with different array types
        """
        return {
            'random': [random.randint(1, 1000) for _ in range(size)],
            'sorted': list(range(1, size + 1)),
            'reverse_sorted': list(range(size, 0, -1)),
            'repeated': [random.randint(1, 10) for _ in range(size)],
            'nearly_sorted': self._generate_nearly_sorted(size)
        }
    
    def _generate_nearly_sorted(self, size: int) -> List[int]:
        """Create array that is mostly sorted with few random swaps"""
        arr = list(range(1, size + 1))
        # Swap 10% of elements randomly
        for _ in range(size // 10):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    
    def benchmark_algorithms(self, sizes: List[int], num_trials: int = 5) -> dict:
        """
        Test both algorithms on different array sizes and types
        
        Parameters:
            sizes: List of array sizes to test
            num_trials: How many times to run each test
            
        Returns:
            Dictionary with all test results
        """
        # Increase recursion limit for deterministic quicksort testing
        original_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(10000)
        
        results = {
            'sizes': sizes,
            'randomized': {'random': [], 'sorted': [], 'reverse_sorted': [], 'repeated': []},
            'deterministic': {'random': [], 'sorted': [], 'reverse_sorted': [], 'repeated': []},
            'comparisons_rand': {'random': [], 'sorted': [], 'reverse_sorted': [], 'repeated': []},
            'comparisons_det': {'random': [], 'sorted': [], 'reverse_sorted': [], 'repeated': []}
        }
        
        for size in sizes:
            print(f"Testing with array size {size}...")
            
            for array_type in ['random', 'sorted', 'reverse_sorted', 'repeated']:
                rand_times = []
                det_times = []
                rand_comps = []
                det_comps = []
                
                for trial in range(num_trials):
                    test_arrays = self.generate_test_arrays(size)
                    
                    # Test Randomized Quicksort
                    arr_copy = test_arrays[array_type].copy()
                    self.reset_comparisons()
                    
                    start_time = time.perf_counter()
                    self.quick_sort_analyzer(arr_copy)
                    end_time = time.perf_counter()
                    
                    rand_times.append(end_time - start_time)
                    rand_comps.append(self.comparisons)
                    
                    # Test Deterministic Quicksort with error handling
                    arr_copy = test_arrays[array_type].copy()
                    self.reset_comparisons()
                    
                    try:
                        start_time = time.perf_counter()
                        self.deterministic_quicksort(arr_copy)
                        end_time = time.perf_counter()
                        
                        det_times.append(end_time - start_time)
                        det_comps.append(self.comparisons)
                    except RecursionError:
                        # Handle recursion error for worst-case scenarios
                        print(f"  Warning: Deterministic quicksort hit recursion limit on {array_type} array size {size}")
                        # Use a very large time to represent poor performance
                        det_times.append(1.0)  # 1 second as penalty
                        det_comps.append(size * size)  # O(n²) comparisons estimate
                
                # Calculate average results
                results['randomized'][array_type].append(np.mean(rand_times))
                results['deterministic'][array_type].append(np.mean(det_times))
                results['comparisons_rand'][array_type].append(np.mean(rand_comps))
                results['comparisons_det'][array_type].append(np.mean(det_comps))
        
        # Restore original recursion limit
        sys.setrecursionlimit(original_limit)
        return results
    
    def plot_results(self, results: dict):
        """Create graphs to show performance comparison"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        sizes = results['sizes']
        array_types = ['random', 'sorted', 'reverse_sorted', 'repeated']
        colors = ['blue', 'green', 'red', 'orange']
        
        # Create separate graph for each array type
        for i, array_type in enumerate(array_types):
            ax = [ax1, ax2, ax3, ax4][i]
            
            ax.plot(sizes, results['randomized'][array_type], 
                   'o-', color=colors[i], label='Randomized', linewidth=2)
            ax.plot(sizes, results['deterministic'][array_type], 
                   's--', color=colors[i], label='Deterministic', linewidth=2)
            
            ax.set_xlabel('Array Size')
            ax.set_ylabel('Time (seconds)')
            ax.set_title(f'{array_type.replace("_", " ").title()} Arrays')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_xscale('log')
            ax.set_yscale('log')
        
        plt.tight_layout()
        
        plt.savefig('results/quicksort_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def theoretical_analysis_demo(self):
        """
        Explain the mathematical analysis behind randomized quicksort
        """
        print("=== MATHEMATICAL ANALYSIS OF RANDOMIZED QUICKSORT ===\n")
        
        print("Why Randomized Quicksort works better:")
        print("=====================================")
        print("The main idea is to avoid worst case scenarios by choosing pivot randomly.")
        print()
        print("Average time complexity calculation:")
        print("If T(n) = time needed to sort n elements, then:")
        print("T(n) = time to split array + time to sort left part + time to sort right part")
        print("T(n) = O(n) + average of all possible splits")
        print()
        print("Mathematical formula:")
        print("T(n) = O(n) + (1/n) * sum of [T(k-1) + T(n-k)] for k=1 to n")
        print()
        print("Here:")
        print("- O(n) = time to split the array")
        print("- (1/n) = probability of choosing any element as pivot")
        print("- T(k-1) + T(n-k) = time to sort left and right parts")
        print()
        print("Using probability theory:")
        print("We count how many times any two elements are compared.")
        print("For elements at positions i and j (where i < j):")
        print("They are compared only if one becomes pivot before others between them")
        print("Probability = 2/(j-i+1)")
        print()
        print("Total expected comparisons:")
        print("Sum over all pairs = approximately 2 * n * log(n)")
        print("This gives us O(n log n) average time")
        print()
        
        # Show practical results
        sizes = [100, 500, 1000, 2000, 5000]
        comparisons = []
        
        for size in sizes:
            total_comps = 0
            trials = 10
            
            for _ in range(trials):
                arr = [random.randint(1, 1000) for _ in range(size)]
                self.reset_comparisons()
                self.quick_sort_analyzer(arr.copy())
                total_comps += self.comparisons
            
            avg_comps = total_comps / trials
            comparisons.append(avg_comps)
            theoretical = size * np.log2(size) * 1.39  # Mathematical prediction
            
            print(f"Array size {size}: Actual comparisons = {avg_comps:.0f}, "
                  f"Theory predicts approximately {theoretical:.0f}, "
                  f"Difference = {avg_comps/theoretical:.2f}")


# Main program execution
if __name__ == "__main__":
    analyzer = QuickSortAnalyzer()
    
    # Show mathematical explanation
    analyzer.theoretical_analysis_demo()
    
    print("\n" + "="*60)
    print("PRACTICAL PERFORMANCE TESTING")
    print("="*60)
    
    # Test different array sizes - reduced for better performance
    sizes = [100, 500, 1000, 1500, 2000]
    print("Note: Using smaller array sizes to avoid recursion issues with deterministic quicksort")
    results = analyzer.benchmark_algorithms(sizes, num_trials=3)
    
    # Create comparison graphs
    analyzer.plot_results(results)
    
    # Show summary of results
    print("\nSummary of Test Results:")
    print("========================")
    for array_type in ['random', 'sorted', 'reverse_sorted', 'repeated']:
        print(f"\n{array_type.replace('_', ' ').title()} Arrays:")
        rand_avg = np.mean(results['randomized'][array_type])
        det_avg = np.mean(results['deterministic'][array_type])
        if det_avg > 0:
            improvement = ((det_avg - rand_avg) / det_avg) * 100
        else:
            improvement = 0
        print(f"  Randomized version average time: {rand_avg:.6f} seconds")
        print(f"  Deterministic version average time: {det_avg:.6f} seconds")
        print(f"  Performance improvement: {improvement:.1f}%")