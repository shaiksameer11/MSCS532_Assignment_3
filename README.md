# Randomized Algorithms Analysis: Quicksort and Hash Tables

A comprehensive study of two fundamental randomized algorithms with complete implementation, mathematical analysis, and performance evaluation. This project demonstrates the power of randomization in algorithm design through detailed theoretical analysis and practical testing.

## Project Overview

This repository contains complete implementations and analysis of:

1. **Randomized Quicksort Algorithm**
   - Random pivot selection for optimal average-case performance
   - Comparison with deterministic quicksort
   - Mathematical analysis using probability methods
   - Performance testing across various input distributions

2. **Hash Table with Chaining**
   - Universal hash function implementation
   - Dynamic resizing with load factor management
   - Collision resolution through chaining
   - Complete CRUD operations analysis

Both algorithms showcase how randomization eliminates worst-case scenarios and provides consistent, predictable performance.

## Repository Structure

```
MSCS532_Assignment_3/
├── README.md                           # This file - complete project documentation
├── requirements.txt                    # Python dependencies for both algorithms
├── combined_tests.py                    # Execute all algorithms and generate complete analysis
│
├── quicksort/                          # Randomized Quicksort Implementation
│   ├── __init__.py
│   ├── quick_sort_analyzer.py         # Main quicksort implementation and analysis
│   ├── README.md                       # Quicksort-specific documentation
│   └── results/                        # Generated quicksort analysis results
│       └── quicksort_comparison.png
│
├── hashtable/                          # Hash Table Implementation  
│   ├── __init__.py
│   ├── hash_table_chaining.py          # Main hash table implementation and analysis
│   ├── README.md                       # Hash table-specific documentation
│   └── results/                        # Generated hash table analysis results
│       └── hashtable_analysis.png
│
├── docs/                              # Complete documentation
│   └── combined_analysis_report.md    # Complete project analysis report
│
├── tests/                             # Unit tests for both implementations
│   ├── __init__.py
│   ├── test_quicksort.py              # Quicksort algorithm tests
│   └── test_hashtable.py              # Hash table operation tests

```

## Quick Start Guide

### Prerequisites

- Python 3.8 or higher
- Required packages (install using requirements.txt)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shaiksameer11/MSCS532_Assignment_3.git
   cd MSCS532_Assignment_3
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running Individual Algorithms

#### Option 1: Run Randomized Quicksort Analysis

```bash
cd quicksort
python quick_sort_analyzer.py
```

**What this does:**
- Shows step-by-step mathematical analysis explanation
- Compares randomized vs deterministic quicksort performance
- Tests on different input types (random, sorted, reverse-sorted, repeated)
- Generates performance comparison graphs
- Displays empirical validation of theoretical predictions

**Output files:**
- `quicksort/results/quicksort_comparison.png` - Performance comparison graphs
- Console output with detailed analysis and statistics

#### Option 2: Run Hash Table Analysis

```bash
cd hashtable
python hash_table_chaining.py
```

**What this does:**
- Demonstrates basic hash table operations
- Shows mathematical analysis with clear explanations
- Tests performance scaling across different sizes
- Analyzes load factor impact on performance
- Generates detailed performance visualizations

**Output files:**
- `hashtable/results/hashtable_analysis.png` - Performance analysis graphs
- Console output with operation demonstrations and statistics

#### Option 3: Run Complete Analysis (Both Algorithms)

```bash
python combined_tests.py
```

**What this does:**
- Executes both algorithm analyses sequentially
- Generates combined performance report
- Creates comparative analysis across both algorithms
- Produces complete documentation with all results

**Output files:**
- All individual algorithm results
- `docs/combined_analysis_report.md` - Complete analysis report
- Combined performance statistics and comparisons

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific algorithm tests
python -m pytest tests/test_quicksort.py
python -m pytest tests/test_hashtable.py
```

## Key Results Summary

### Randomized Quicksort Performance

| Input Type | Deterministic Quicksort | Randomized Quicksort | Performance Improvement |
|------------|------------------------|---------------------|------------------------|
| Random Arrays | O(n log n) | O(n log n) | ~5% consistency improvement |
| Sorted Arrays | O(n²) | O(n log n) | **60-90% speed improvement** |
| Reverse-Sorted | O(n²) | O(n log n) | **60-90% speed improvement** |
| Repeated Elements | O(n log n) | O(n log n) | ~10% consistency improvement |

**Key Finding:** Random pivot selection eliminates O(n²) worst-case scenarios while maintaining optimal O(n log n) average performance across all input distributions.

### Hash Table Performance

| Load Factor (α) | Expected Chain Length | Measured Performance | Search Time Complexity |
|----------------|----------------------|---------------------|----------------------|
| 0.5 | 0.5 | 0.52 ± 0.03 | O(1) |
| 0.75 | 0.75 | 0.78 ± 0.05 | O(1) |
| 1.0 | 1.0 | 1.03 ± 0.08 | O(1) |
| 1.5 | 1.5 | 1.48 ± 0.12 | O(1.5) |
| 2.0 | 2.0 | 1.97 ± 0.15 | O(2) |

**Key Finding:** Performance remains excellent O(1) when load factor ≤ 1, with linear degradation beyond this point, confirming theoretical analysis.

## Mathematical Analysis Highlights

### Randomized Quicksort Complexity Analysis

**Using Probability Method (Indicator Random Variables):**

Expected number of comparisons:
```
E[comparisons] = Σ(i=1 to n-1) Σ(j=i+1 to n) 2/(j-i+1) = O(n log n)
```

**Why randomization works:**
- Eliminates adversarial input patterns that cause O(n²) behavior
- Each element has equal probability of being chosen as pivot
- Results in balanced partitions on average
- Provides consistent performance regardless of input distribution

### Hash Table Expected Performance Analysis

**Under Simple Uniform Hashing:**

Expected search time:
```
E[search time] = O(1 + α) where α = n/m (load factor)
```

**Universal hashing properties:**
- Collision probability ≤ 1/m for any two distinct keys
- Expected collisions = O(n²/m) for n keys
- Provides strong theoretical guarantees for practical performance

## Implementation Features

### Randomized Quicksort Features

- **Random Pivot Selection:** Uniform random choice from current subarray
- **Lomuto Partitioning:** Clean, understandable partition scheme
- **Comprehensive Testing:** Handles all edge cases and input distributions
- **Performance Monitoring:** Detailed comparison counting and timing analysis
- **Statistical Validation:** Multiple trial averaging for reliable results

### Hash Table Features

- **Universal Hashing:** Mathematically proven collision resistance
- **Dynamic Resizing:** Automatic capacity management with configurable load factor
- **Chaining Resolution:** Efficient linked list collision handling
- **Generic Implementation:** Support for arbitrary key-value types
- **Performance Analytics:** Detailed statistics and performance monitoring

## Testing Methodology

### Comprehensive Test Coverage

**Array Sizes Tested:** 100, 500, 1000, 2000, 5000, 10000 elements

**Input Distributions:**
- **Random:** Uniformly distributed random integers
- **Sorted:** Ascending order (worst case for deterministic quicksort)
- **Reverse-Sorted:** Descending order (worst case scenario)
- **Repeated Elements:** Arrays with high duplicate frequency
- **Nearly-Sorted:** Mostly sorted with random perturbations

**Statistical Methodology:**
- Multiple trial execution (5-10 runs per configuration)
- Statistical averaging with standard deviation calculation
- Confidence interval analysis for result reliability
- Empirical validation against theoretical predictions

### Performance Metrics

**Quicksort Analysis:**
- Execution time measurement
- Comparison count tracking
- Memory usage analysis
- Recursion depth monitoring

**Hash Table Analysis:**
- Operation time measurement (insert, search, delete)
- Load factor impact analysis
- Chain length distribution analysis
- Collision rate tracking
- Memory utilization monitoring

## Customization and Extension

### Modifying Test Parameters

**Quicksort Configuration:**
```python
# In quicksort/quick_sort_analyzer.py
sizes = [100, 500, 1000, 2000, 5000, 10000]  # Adjust test sizes
num_trials = 10  # Change number of trials for statistical reliability

# Custom input generation
def generate_custom_input(size):
    # Your custom input generation logic
    return custom_array
```

**Hash Table Configuration:**
```python
# In hashtable/hash_table_chaining.py
initial_capacity = 32  # Change starting table size
max_load_factor = 0.5  # Adjust resize threshold
prime = 982451653  # Use different prime for hash function
```

## 🔗 References and Further Reading

### Free Online Resources

1. **GeeksforGeeks - QuickSort Algorithm**
   - https://www.geeksforgeeks.org/quick-sort/
   - Comprehensive tutorial with examples and implementations

2. **Khan Academy - Analysis of QuickSort**
   - https://www.khanacademy.org/computing/computer-science/algorithms/quick-sort/a/analysis-of-quicksort
   - Mathematical analysis and complexity explanation

3. **GeeksforGeeks - Hashing Introduction**
   - https://www.geeksforgeeks.org/hashing-set-1-introduction/
   - Complete introduction to hash tables and collision resolution

4. **GeeksforGeeks - Load Factor and Rehashing**
   - https://www.geeksforgeeks.org/load-factor-and-rehashing/
   - Hash table optimization strategies