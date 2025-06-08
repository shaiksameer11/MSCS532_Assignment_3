# tests/test_hashtable.py
"""
Unit tests for Hash Table with Chaining implementation
Tests correctness, edge cases, and basic performance characteristics
"""

import unittest
import sys
import os
import random
import string

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'hashtable'))

from hash_table_chaining import HashTableChaining, HashNode

class TestHashTableChaining(unittest.TestCase):
    """Test cases for Hash Table with Chaining implementation"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.ht = HashTableChaining()
        
    def test_basic_insert_and_search(self):
        """Test basic insert and search operations"""
        # Insert single key-value pair
        self.ht.insert("key1", "value1")
        result = self.ht.search("key1")
        self.assertEqual(result, "value1")
        
        # Search for non-existent key
        result = self.ht.search("nonexistent")
        self.assertIsNone(result)
        
    def test_multiple_insertions(self):
        """Test multiple insertions and searches"""
        test_data = [
            ("apple", 5),
            ("banana", 3),
            ("cherry", 8),
            ("date", 2),
            ("elderberry", 9)
        ]
        
        # Insert all data
        for key, value in test_data:
            self.ht.insert(key, value)
            
        # Verify all data can be retrieved
        for key, expected_value in test_data:
            result = self.ht.search(key)
            self.assertEqual(result, expected_value)
            
    def test_update_existing_key(self):
        """Test updating value for existing key"""
        self.ht.insert("key1", "value1")
        self.ht.insert("key1", "updated_value")
        
        result = self.ht.search("key1")
        self.assertEqual(result, "updated_value")
        self.assertEqual(self.ht.size, 1)  # Size should not increase
        
    def test_delete_operations(self):
        """Test delete operations"""
        # Insert test data
        self.ht.insert("key1", "value1")
        self.ht.insert("key2", "value2")
        self.ht.insert("key3", "value3")
        
        # Delete existing key
        result = self.ht.delete("key2")
        self.assertTrue(result)
        self.assertIsNone(self.ht.search("key2"))
        self.assertEqual(self.ht.size, 2)
        
        # Try to delete non-existent key
        result = self.ht.delete("nonexistent")
        self.assertFalse(result)
        self.assertEqual(self.ht.size, 2)
        
        # Verify other keys still exist
        self.assertEqual(self.ht.search("key1"), "value1")
        self.assertEqual(self.ht.search("key3"), "value3")
        
    def test_empty_hash_table(self):
        """Test operations on empty hash table"""
        # Search in empty table
        result = self.ht.search("any_key")
        self.assertIsNone(result)
        
        # Delete from empty table
        result = self.ht.delete("any_key")
        self.assertFalse(result)
        
        # Check initial state
        self.assertEqual(self.ht.size, 0)
        self.assertEqual(self.ht.get_load_factor(), 0.0)
        
    def test_load_factor_calculation(self):
        """Test load factor calculation"""
        initial_capacity = self.ht.capacity
        
        # Add elements and check load factor
        for i in range(5):
            self.ht.insert(f"key{i}", f"value{i}")
            expected_load_factor = (i + 1) / initial_capacity
            self.assertAlmostEqual(self.ht.get_load_factor(), expected_load_factor, places=2)
            
    def test_automatic_resizing(self):
        """Test automatic resizing when load factor exceeds threshold"""
        initial_capacity = self.ht.capacity
        max_load_factor = self.ht.max_load_factor
        
        # Add enough elements to trigger resize
        num_elements = int(initial_capacity * max_load_factor) + 1
        
        for i in range(num_elements):
            self.ht.insert(f"key{i}", f"value{i}")
            
        # Check that table was resized
        self.assertGreater(self.ht.capacity, initial_capacity)
        self.assertEqual(self.ht.resize_count, 1)
        
        # Verify all elements still retrievable after resize
        for i in range(num_elements):
            result = self.ht.search(f"key{i}")
            self.assertEqual(result, f"value{i}")
            
    def test_different_key_types(self):
        """Test hash table with different key types"""
        test_cases = [
            ("string_key", "string_value"),
            (42, "integer_key_value"),
            ((1, 2), "tuple_key_value"),
        ]
        
        for key, value in test_cases:
            self.ht.insert(key, value)
            result = self.ht.search(key)
            self.assertEqual(result, value)
        
    def test_statistics_collection(self):
        """Test statistics collection functionality"""
        # Add some test data
        for i in range(10):
            self.ht.insert(f"key{i}", f"value{i}")
            
        stats = self.ht.get_statistics()
        
        # Check that all expected statistics are present
        expected_keys = [
            'size', 'capacity', 'load_factor', 'collision_count',
            'resize_count', 'total_operations', 'max_chain_length',
            'avg_chain_length', 'empty_slots', 'collision_rate'
        ]
        
        for key in expected_keys:
            self.assertIn(key, stats)
            
        # Verify some basic relationships
        self.assertEqual(stats['size'], 10)
        self.assertGreaterEqual(stats['collision_count'], 0)
        self.assertGreaterEqual(stats['total_operations'], 10)
        
    def test_large_dataset(self):
        """Test with larger dataset for performance verification"""
        num_elements = 1000
        
        # Insert large number of elements
        for i in range(num_elements):
            key = ''.join(random.choices(string.ascii_letters, k=10))
            value = random.randint(1, 1000)
            self.ht.insert(key, value)
            
        # Verify final size
        self.assertEqual(self.ht.size, num_elements)
        
        # Check that load factor is maintained
        self.assertLessEqual(self.ht.get_load_factor(), self.ht.max_load_factor * 1.1)

class TestHashNode(unittest.TestCase):
    """Test cases for HashNode class"""
    
    def test_node_creation(self):
        """Test hash node creation"""
        node = HashNode("test_key", "test_value")
        
        self.assertEqual(node.key, "test_key")
        self.assertEqual(node.value, "test_value")
        self.assertIsNone(node.next)
        
    def test_node_linking(self):
        """Test linking hash nodes"""
        node1 = HashNode("key1", "value1")
        node2 = HashNode("key2", "value2")
        
        node1.next = node2
        
        self.assertEqual(node1.next, node2)
        self.assertIsNone(node2.next)


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)