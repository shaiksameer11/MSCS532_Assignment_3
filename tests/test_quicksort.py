# tests/test_quicksort.py
"""
Unit tests for Randomized Quicksort implementation
Tests correctness, edge cases, and basic performance characteristics
"""

import unittest
import sys
import os
import random

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'quicksort'))

from quick_sort_analyzer import QuickSortAnalyzer

class TestRandomizedQuicksort(unittest.TestCase):
    """Test cases for Randomized Quicksort implementation"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.analyzer = QuickSortAnalyzer()
        
    def test_empty_array(self):
        """Test sorting empty array"""
        arr = []
        result = self.analyzer.quick_sort_analyzer(arr.copy())
        self.assertEqual(result, [])
        
    def test_single_element(self):
        """Test sorting single element array"""
        arr = [42]
        result = self.analyzer.quick_sort_analyzer(arr.copy())
        self.assertEqual(result, [42])
        
    def test_two_elements(self):
        """Test sorting two element arrays"""
        # Already sorted
        arr = [1, 2]
        result = self.analyzer.quick_sort_analyzer(arr.copy())
        self.assertEqual(result, [1, 2])
        
        # Reverse sorted
        arr = [2, 1]
        result = self.analyzer.quick_sort_analyzer(arr.copy())
        self.assertEqual(result, [1, 2])
        
    def test_sorted_array(self):
        """Test sorting already sorted array"""
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = self.analyzer.quick_sort_analyzer(arr.copy())
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        
    def test_reverse_sorted_array(self):
        """Test sorting reverse sorted array"""
        arr = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        result = self.analyzer.quick_sort_analyzer(arr.copy())
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        
    def test_duplicate_elements(self):
        """Test sorting array with duplicate elements"""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        result = self.analyzer.quick_sort_analyzer(arr.copy())
        expected = [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]
        self.assertEqual(result, expected)
        
    def test_all_same_elements(self):
        """Test sorting array with all identical elements"""
        arr = [5, 5, 5, 5, 5]
        result = self.analyzer.quick_sort_analyzer(arr.copy())
        self.assertEqual(result, [5, 5, 5, 5, 5])
        
    def test_random_array(self):
        """Test sorting random array"""
        arr = [random.randint(1, 100) for _ in range(20)]
        original = arr.copy()
        result = self.analyzer.quick_sort_analyzer(arr.copy())
        
        # Check that result is sorted
        self.assertEqual(result, sorted(original))
        
    def test_negative_numbers(self):
        """Test sorting array with negative numbers"""
        arr = [-3, 1, -4, 1, 5, -9, 2, 6, -5, 3]
        result = self.analyzer.quick_sort_analyzer(arr.copy())
        expected = [-9, -5, -4, -3, 1, 1, 2, 3, 5, 6]
        self.assertEqual(result, expected)
        
    def test_large_array(self):
        """Test sorting larger array"""
        arr = [random.randint(1, 1000) for _ in range(100)]
        original = arr.copy()
        result = self.analyzer.quick_sort_analyzer(arr.copy())
        
        # Check that result is sorted
        self.assertEqual(result, sorted(original))
        
    def test_deterministic_vs_randomized(self):
        """Test that both algorithms produce same sorted result"""
        test_arrays = [
            [3, 1, 4, 1, 5, 9, 2, 6, 5],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [random.randint(1, 50) for _ in range(30)]
        ]
        
        for arr in test_arrays:
            rand_result = self.analyzer.quick_sort_analyzer(arr.copy())
            det_result = self.analyzer.deterministic_quicksort(arr.copy())
            expected = sorted(arr)
            
            self.assertEqual(rand_result, expected)
            self.assertEqual(det_result, expected)
            
    def test_comparison_counting(self):
        """Test that comparison counting works"""
        arr = [3, 1, 4, 1, 5]
        
        self.analyzer.reset_comparisons()
        self.analyzer.quick_sort_analyzer(arr.copy())
        comparisons = self.analyzer.comparisons
        
        # Should have made some comparisons
        self.assertGreater(comparisons, 0)
        self.assertLessEqual(comparisons, len(arr) * len(arr))  # Upper bound check
        
    def test_generate_test_arrays(self):
        """Test test array generation methods"""
        size = 10
        arrays = self.analyzer.generate_test_arrays(size)
        
        # Check all expected array types are generated
        expected_types = ['random', 'sorted', 'reverse_sorted', 'repeated', 'nearly_sorted']
        for array_type in expected_types:
            self.assertIn(array_type, arrays)
            self.assertEqual(len(arrays[array_type]), size)
            
        # Check sorted array is actually sorted
        self.assertEqual(arrays['sorted'], list(range(1, size + 1)))
        
        # Check reverse sorted array
        self.assertEqual(arrays['reverse_sorted'], list(range(size, 0, -1)))