import random
import time
import matplotlib.pyplot as plt
import numpy as np
from typing import Any, Optional, List, Tuple
import os

class HashNode:
    """Single node in the chain for hash table"""
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.next: Optional['HashNode'] = None

class HashTableChaining:
    """
    Hash Table using chaining method to handle collisions
    Uses universal hashing and can resize automatically
    """
    
    def __init__(self, initial_capacity: int = 16, max_load_factor: float = 0.75):
        """
        Create new hash table
        
        Parameters:
            initial_capacity: Starting size of hash table
            max_load_factor: When to resize (0.75 means resize when 75% full)
        """
        self.capacity = initial_capacity
        self.size = 0
        self.max_load_factor = max_load_factor
        self.table: List[Optional[HashNode]] = [None] * self.capacity
        
        # Parameters for universal hash function
        self._generate_hash_params()
        
        # Keep track of performance statistics
        self.collision_count = 0
        self.resize_count = 0
        self.total_operations = 0
        
    def _generate_hash_params(self):
        """Create random parameters for hash function"""
        # Use large prime number for better distribution
        self.prime = 1000000007
        # Choose random numbers for universal hashing formula
        self.a = random.randint(1, self.prime - 1)
        self.b = random.randint(0, self.prime - 1)
    
    def _hash(self, key: Any) -> int:
        """
        Universal hash function: converts key to array index
        Formula: h(k) = ((a*k + b) mod p) mod m
        
        Parameters:
            key: Key to convert to index
            
        Returns:
            Index in range [0, capacity-1]
        """
        if isinstance(key, str):
            # Convert string to number using character values
            hash_val = 0
            for char in key:
                hash_val = (hash_val * 31 + ord(char)) % self.prime
        else:
            hash_val = hash(key) % self.prime
            
        return ((self.a * hash_val + self.b) % self.prime) % self.capacity
    
    def _resize(self):
        """Make hash table bigger when it gets too full"""
        old_table = self.table
        old_capacity = self.capacity
        
        # Make table twice as big
        self.capacity *= 2
        self.size = 0
        self.table = [None] * self.capacity
        self.resize_count += 1
        
        # Create new hash parameters for new size
        self._generate_hash_params()
        
        # Move all existing elements to new table
        for head in old_table:
            current = head
            while current:
                self._insert_node(current.key, current.value)
                current = current.next
    
    def insert(self, key: Any, value: Any):
        """
        Add key-value pair to hash table
        
        Parameters:
            key: Key to add
            value: Value to store with this key
        """
        self.total_operations += 1
        
        # Check if we need to make table bigger
        if self.size >= self.capacity * self.max_load_factor:
            self._resize()
        
        self._insert_node(key, value)
    
    def _insert_node(self, key: Any, value: Any):
        """Helper method to add node without checking resize"""
        index = self._hash(key)
        
        # If slot is empty, create new node
        if self.table[index] is None:
            self.table[index] = HashNode(key, value)
            self.size += 1
            return
        
        # Check if key already exists and update its value
        current = self.table[index]
        while current:
            if current.key == key:
                current.value = value  # Update existing key
                return
            if current.next is None:
                break
            current = current.next
        
        # Add new node at end of chain (collision happened)
        self.collision_count += 1
        current.next = HashNode(key, value)
        self.size += 1
    
    def search(self, key: Any) -> Optional[Any]:
        """
        Find value for given key
        
        Parameters:
            key: Key to search for
            
        Returns:
            Value if found, None if not found
        """
        self.total_operations += 1
        index = self._hash(key)
        
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        
        return None
    
    def delete(self, key: Any) -> bool:
        """
        Remove key-value pair from hash table
        
        Parameters:
            key: Key to remove
            
        Returns:
            True if key was found and removed, False if not found
        """
        self.total_operations += 1
        index = self._hash(key)
        
        current = self.table[index]
        prev = None
        
        while current:
            if current.key == key:
                if prev is None:
                    # Removing first node in chain
                    self.table[index] = current.next
                else:
                    # Removing middle or end node
                    prev.next = current.next
                self.size -= 1
                return True
            prev = current
            current = current.next
        
        return False
    
    def get_load_factor(self) -> float:
        """Calculate how full the hash table is"""
        return self.size / self.capacity
    
    def get_chain_lengths(self) -> List[int]:
        """Get length of chain at each position for analysis"""
        lengths = []
        for head in self.table:
            length = 0
            current = head
            while current:
                length += 1
                current = current.next
            lengths.append(length)
        return lengths
    
    def get_statistics(self) -> dict:
        """Get detailed information about hash table performance"""
        chain_lengths = self.get_chain_lengths()
        non_empty_chains = [l for l in chain_lengths if l > 0]
        
        return {
            'size': self.size,
            'capacity': self.capacity,
            'load_factor': self.get_load_factor(),
            'collision_count': self.collision_count,
            'resize_count': self.resize_count,
            'total_operations': self.total_operations,
            'max_chain_length': max(chain_lengths) if chain_lengths else 0,
            'avg_chain_length': np.mean(non_empty_chains) if non_empty_chains else 0,
            'empty_slots': chain_lengths.count(0),
            'collision_rate': self.collision_count / self.total_operations if self.total_operations > 0 else 0
        }
    
    def display_table(self):
        """Show hash table contents for debugging"""
        print(f"Hash Table (Size: {self.size}, Capacity: {self.capacity}, "
              f"Load Factor: {self.get_load_factor():.2f})")
        print("=" * 50)
        
        for i, head in enumerate(self.table):
            if head is not None:
                chain = []
                current = head
                while current:
                    chain.append(f"({current.key}: {current.value})")
                    current = current.next
                print(f"Position {i}: {' -> '.join(chain)}")


class HashTableAnalyzer:
    """Class to test and analyze hash table performance"""
    
    def benchmark_operations(self, sizes: List[int], num_trials: int = 5) -> dict:
        """
        Test hash table performance with different sizes
        
        Parameters:
            sizes: List of sizes to test
            num_trials: How many times to run each test
            
        Returns:
            Dictionary with all test results
        """
        results = {
            'sizes': sizes,
            'insert_times': [],
            'search_times': [],
            'delete_times': [],
            'load_factors': [],
            'chain_lengths': [],
            'collision_rates': []
        }
        
        for size in sizes:
            print(f"Testing with {size} elements...")
            
            insert_times = []
            search_times = []
            delete_times = []
            load_factors = []
            chain_lengths = []
            collision_rates = []
            
            for trial in range(num_trials):
                # Create hash table
                ht = HashTableChaining()
                
                # Create test data
                keys = [f"key_{i}" for i in range(size)]
                values = [f"value_{i}" for i in range(size)]
                
                # Test insertion speed
                start_time = time.perf_counter()
                for key, value in zip(keys, values):
                    ht.insert(key, value)
                insert_time = time.perf_counter() - start_time
                insert_times.append(insert_time)
                
                # Test search speed
                search_keys = random.sample(keys, min(1000, size))
                start_time = time.perf_counter()
                for key in search_keys:
                    ht.search(key)
                search_time = time.perf_counter() - start_time
                search_times.append(search_time / len(search_keys))  # Per operation
                
                # Test deletion speed
                delete_keys = random.sample(keys, min(100, size // 10))
                start_time = time.perf_counter()
                for key in delete_keys:
                    ht.delete(key)
                delete_time = time.perf_counter() - start_time
                delete_times.append(delete_time / len(delete_keys))  # Per operation
                
                # Collect statistics
                stats = ht.get_statistics()
                load_factors.append(stats['load_factor'])
                chain_lengths.append(stats['avg_chain_length'])
                collision_rates.append(stats['collision_rate'])
            
            # Store average results
            results['insert_times'].append(np.mean(insert_times))
            results['search_times'].append(np.mean(search_times))
            results['delete_times'].append(np.mean(delete_times))
            results['load_factors'].append(np.mean(load_factors))
            results['chain_lengths'].append(np.mean(chain_lengths))
            results['collision_rates'].append(np.mean(collision_rates))
        
        return results
    
    def analyze_load_factor_impact(self, base_size: int = 1000) -> dict:
        """
        See how load factor affects performance
        
        Parameters:
            base_size: Base number of elements for testing
            
        Returns:
            Dictionary with analysis results
        """
        load_factors = np.arange(0.1, 2.1, 0.1)
        results = {
            'load_factors': load_factors,
            'search_times': [],
            'chain_lengths': [],
            'collision_rates': []
        }
        
        for lf in load_factors:
            # Create hash table with specific load factor
            capacity = max(16, int(base_size / lf))
            ht = HashTableChaining(initial_capacity=capacity, max_load_factor=10.0)  # Prevent auto-resize
            
            # Add elements to get target load factor
            num_elements = int(capacity * lf)
            keys = [f"key_{i}" for i in range(num_elements)]
            values = [f"value_{i}" for i in range(num_elements)]
            
            for key, value in zip(keys, values):
                ht.insert(key, value)
            
            # Test search time
            search_keys = random.sample(keys, min(1000, num_elements))
            start_time = time.perf_counter()
            for key in search_keys:
                ht.search(key)
            search_time = (time.perf_counter() - start_time) / len(search_keys)
            
            # Collect statistics
            stats = ht.get_statistics()
            
            results['search_times'].append(search_time)
            results['chain_lengths'].append(stats['avg_chain_length'])
            results['collision_rates'].append(stats['collision_rate'])
        
        return results
    
    def plot_results(self, benchmark_results: dict, load_factor_results: dict):
        """Create graphs showing analysis results"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Graph 1: Operation times vs size
        sizes = benchmark_results['sizes']
        ax1.plot(sizes, benchmark_results['insert_times'], 'o-', label='Insert', linewidth=2)
        ax1.plot(sizes, benchmark_results['search_times'], 's-', label='Search', linewidth=2)
        ax1.plot(sizes, benchmark_results['delete_times'], '^-', label='Delete', linewidth=2)
        ax1.set_xlabel('Hash Table Size')
        ax1.set_ylabel('Time per Operation (seconds)')
        ax1.set_title('Operation Times vs Size')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        
        # Graph 2: Load factor vs size
        ax2.plot(sizes, benchmark_results['load_factors'], 'o-', color='red', linewidth=2)
        ax2.axhline(y=0.75, color='gray', linestyle='--', label='Target Load Factor')
        ax2.set_xlabel('Hash Table Size')
        ax2.set_ylabel('Load Factor')
        ax2.set_title('Load Factor vs Size')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Graph 3: Search time vs load factor
        load_factors = load_factor_results['load_factors']
        ax3.plot(load_factors, load_factor_results['search_times'], 'o-', color='green', linewidth=2)
        ax3.set_xlabel('Load Factor')
        ax3.set_ylabel('Search Time per Operation (seconds)')
        ax3.set_title('Search Performance vs Load Factor')
        ax3.grid(True, alpha=0.3)
        
        # Graph 4: Chain length vs load factor
        ax4.plot(load_factors, load_factor_results['chain_lengths'], 'o-', color='purple', linewidth=2)
        ax4.set_xlabel('Load Factor')
        ax4.set_ylabel('Average Chain Length')
        ax4.set_title('Chain Length vs Load Factor')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/hashtable_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def theoretical_analysis_demo(self):
        """Explain the mathematical theory behind hash tables"""
        print("=== MATHEMATICAL ANALYSIS OF HASH TABLE WITH CHAINING ===\n")
        
        print("How Hash Tables Work:")
        print("====================")
        print("Hash table uses a function to convert keys into array positions.")
        print("When two keys get same position (collision), we use chains (linked lists).")
        print()
        print("Mathematical Analysis (Simple Uniform Hashing):")
        print("==============================================")
        print("We assume each key has equal chance to go to any position.")
        print("Load factor alpha = n/m (n = number of elements, m = table size)")
        print()
        print("Expected chain length: E[chain length] = alpha")
        print("This means if alpha = 1, average chain has 1 element")
        print()
        print("Time Complexity for Operations:")
        print("- Insert: O(1) expected (just add to front or end of chain)")
        print("- Search: O(1 + alpha) expected (check chain of average length alpha)")
        print("- Delete: O(1 + alpha) expected (search + remove)")
        print()
        print("Load Factor Impact:")
        print("- alpha < 1: Very good performance, most chains short")
        print("- alpha = 1: Good performance, average chain length is 1")
        print("- alpha > 1: Performance gets worse linearly with alpha")
        print("- alpha >> 1: Poor performance, like searching in linked list")
        print()
        
        # Show practical results
        print("Practical Verification:")
        print("======================")
        
        # Test different load factors
        for alpha in [0.5, 1.0, 1.5, 2.0]:
            ht = HashTableChaining(initial_capacity=100, max_load_factor=10.0)
            
            # Add elements to get target load factor
            num_elements = int(100 * alpha)
            for i in range(num_elements):
                ht.insert(f"key_{i}", f"value_{i}")
            
            stats = ht.get_statistics()
            
            print(f"Load Factor alpha = {alpha:.1f}:")
            print(f"  Theory says chain length: {alpha:.1f}")
            print(f"  Actual average chain length: {stats['avg_chain_length']:.2f}")
            print(f"  Maximum chain length: {stats['max_chain_length']}")
            print(f"  Collision rate: {stats['collision_rate']:.2%}")
            print()


# Main program execution
if __name__ == "__main__":
    # Test basic operations first
    print("=== BASIC HASH TABLE OPERATIONS TEST ===")
    ht = HashTableChaining()
    
    # Test adding items
    print("Testing insertions...")
    test_data = [("apple", 5), ("banana", 3), ("cherry", 8), ("date", 2), ("elderberry", 9)]
    
    for key, value in test_data:
        ht.insert(key, value)
        print(f"Added {key}: {value}")
    
    print(f"\nHash table size: {ht.size}")
    print(f"Load factor: {ht.get_load_factor():.2f}")
    
    # Test searching
    print("\nTesting searches...")
    for key, expected_value in test_data:
        result = ht.search(key)
        print(f"Search {key}: {result} (expected: {expected_value})")
    
    # Test searching for item that doesn't exist
    result = ht.search("grape")
    print(f"Search grape: {result} (expected: None)")
    
    # Test deletions
    print("\nTesting deletions...")
    print(f"Delete banana: {ht.delete('banana')}")
    print(f"Delete grape (doesn't exist): {ht.delete('grape')}")
    print(f"Search banana after deletion: {ht.search('banana')}")
    
    print(f"\nFinal hash table size: {ht.size}")
    ht.display_table()
    
    print("\n" + "="*60)
    
    # Show mathematical explanation
    analyzer = HashTableAnalyzer()
    analyzer.theoretical_analysis_demo()
    
    print("\n" + "="*60)
    print("PRACTICAL PERFORMANCE TESTING")
    print("="*60)
    
    # Test performance with different sizes
    sizes = [100, 500, 1000, 5000, 10000]
    benchmark_results = analyzer.benchmark_operations(sizes, num_trials=3)
    
    # Test how load factor affects performance
    load_factor_results = analyzer.analyze_load_factor_impact(1000)
    
    # Create comparison graphs
    analyzer.plot_results(benchmark_results, load_factor_results)
    
    # Show summary
    print("\nPerformance Summary:")
    print("===================")
    for i, size in enumerate(sizes):
        print(f"Size {size}:")
        print(f"  Insert time: {benchmark_results['insert_times'][i]:.6f} seconds")
        print(f"  Search time: {benchmark_results['search_times'][i]:.8f} seconds per operation")
        print(f"  Delete time: {benchmark_results['delete_times'][i]:.8f} seconds per operation")
        print(f"  Load factor: {benchmark_results['load_factors'][i]:.2f}")
        print(f"  Average chain length: {benchmark_results['chain_lengths'][i]:.2f}")
        print(f"  Collision rate: {benchmark_results['collision_rates'][i]:.2%}")
        print()