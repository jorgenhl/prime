"""Unit tests for prime_finder module."""

import unittest
from src.prime_finder import is_prime, find_primes_up_to, find_n_primes


class TestIsPrime(unittest.TestCase):
    """Test cases for is_prime function."""

    def test_negative_numbers(self):
        """Negative numbers should not be prime."""
        self.assertFalse(is_prime(-5))
        self.assertFalse(is_prime(-1))

    def test_zero_and_one(self):
        """Zero and one should not be prime."""
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))

    def test_two_is_prime(self):
        """Two is the only even prime."""
        self.assertTrue(is_prime(2))

    def test_even_numbers(self):
        """Even numbers greater than 2 should not be prime."""
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(6))
        self.assertFalse(is_prime(100))

    def test_small_primes(self):
        """Test known small prime numbers."""
        small_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        for prime in small_primes:
            self.assertTrue(is_prime(prime), f"{prime} should be prime")

    def test_composite_numbers(self):
        """Test known composite numbers."""
        composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 25, 27]
        for composite in composites:
            self.assertFalse(is_prime(composite),
                             f"{composite} should not be prime")

    def test_large_prime(self):
        """Test a larger prime number."""
        self.assertTrue(is_prime(97))
        self.assertTrue(is_prime(541))

    def test_large_composite(self):
        """Test a larger composite number."""
        self.assertFalse(is_prime(100))
        self.assertFalse(is_prime(1000))


class TestFindPrimesUpTo(unittest.TestCase):
    """Test cases for find_primes_up_to function."""

    def test_primes_up_to_zero(self):
        """No primes up to 0."""
        self.assertEqual(find_primes_up_to(0), [])

    def test_primes_up_to_one(self):
        """No primes up to 1."""
        self.assertEqual(find_primes_up_to(1), [])

    def test_primes_up_to_two(self):
        """Primes up to 2 should be [2]."""
        self.assertEqual(find_primes_up_to(2), [2])

    def test_primes_up_to_ten(self):
        """Primes up to 10."""
        self.assertEqual(find_primes_up_to(10), [2, 3, 5, 7])

    def test_primes_up_to_thirty(self):
        """Primes up to 30."""
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        self.assertEqual(find_primes_up_to(30), expected)

    def test_primes_up_to_two_is_inclusive(self):
        """Limit should be inclusive."""
        self.assertIn(2, find_primes_up_to(2))
        self.assertIn(3, find_primes_up_to(3))

    def test_all_results_are_prime(self):
        """All results should be prime numbers."""
        primes = find_primes_up_to(50)
        for prime in primes:
            self.assertTrue(is_prime(prime))

    def test_no_composites_returned(self):
        """No composite numbers should be returned."""
        primes = find_primes_up_to(30)
        composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 25, 27]
        for composite in composites:
            if composite <= 30:
                self.assertNotIn(composite, primes)


class TestFindNPrimes(unittest.TestCase):
    """Test cases for find_n_primes function."""

    def test_find_zero_primes(self):
        """Finding 0 primes should return empty list."""
        self.assertEqual(find_n_primes(0), [])

    def test_find_one_prime(self):
        """First prime is 2."""
        self.assertEqual(find_n_primes(1), [2])

    def test_find_five_primes(self):
        """First 5 primes."""
        self.assertEqual(find_n_primes(5), [2, 3, 5, 7, 11])

    def test_find_ten_primes(self):
        """First 10 primes."""
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        self.assertEqual(find_n_primes(10), expected)

    def test_all_results_are_prime(self):
        """All results should be prime numbers."""
        primes = find_n_primes(20)
        for prime in primes:
            self.assertTrue(is_prime(prime))

    def test_correct_count_returned(self):
        """Should return exactly N primes."""
        for n in [1, 5, 10, 15, 20]:
            primes = find_n_primes(n)
            self.assertEqual(len(primes), n)

    def test_returns_first_primes_in_order(self):
        """Primes should be in ascending order."""
        primes = find_n_primes(10)
        self.assertEqual(primes, sorted(primes))

    def test_no_duplicates(self):
        """No duplicate primes should be returned."""
        primes = find_n_primes(20)
        self.assertEqual(len(primes), len(set(primes)))


if __name__ == "__main__":
    unittest.main()
