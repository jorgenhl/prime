# Testing Documentation

## Overview

This document describes the testing approach for the Prime Finder project. We use Python's
built-in `unittest` framework with `pytest` as the test runner.

## Test Structure

Tests are organized in `test_prime_finder.py` with three main test classes:

### 1. TestIsPrime (8 tests)

Tests for the `is_prime(n)` function that determines if a number is prime.

#### Edge Cases

- `test_negative_numbers`: Negative numbers are not prime
- `test_zero_and_one`: 0 and 1 are not prime
- `test_two_is_prime`: 2 is the only even prime number

#### Correctness

- `test_even_numbers`: Even numbers > 2 are not prime
- `test_small_primes`: Validates known small primes (3, 5, 7, 11, ..., 31)
- `test_composite_numbers`: Tests 14 known composite numbers
- `test_large_prime`: Tests larger primes (97, 541)
- `test_large_composite`: Tests larger composites (100, 1000)

### 2. TestFindPrimesUpTo (8 tests)

Tests for the `find_primes_up_to(limit)` function that returns all primes up to a limit.

#### Boundary Conditions

- `test_primes_up_to_zero`: Empty result for limit 0
- `test_primes_up_to_one`: Empty result for limit 1
- `test_primes_up_to_two`: Returns [2] for limit 2
- `test_primes_up_to_two_is_inclusive`: Limit is inclusive

#### Correctness

- `test_primes_up_to_ten`: Validates result for limit 10 is [2, 3, 5, 7]
- `test_primes_up_to_thirty`: Validates result for limit 30
- `test_all_results_are_prime`: All returned values pass `is_prime()`
- `test_no_composites_returned`: No composite numbers in results

### 3. TestFindNPrimes (8 tests)

Tests for the `find_n_primes(count)` function that returns the first N primes.

#### Boundary Conditions

- `test_find_zero_primes`: Empty list for count 0
- `test_find_one_prime`: Returns [2] for count 1
- `test_correct_count_returned`: Verifies exact count (n=1,5,10,15,20)

#### Correctness

- `test_find_five_primes`: Validates first 5 primes [2, 3, 5, 7, 11]
- `test_find_ten_primes`: Validates first 10 primes
- `test_all_results_are_prime`: All returned values pass `is_prime()`
- `test_returns_first_primes_in_order`: Results are in ascending order
- `test_no_duplicates`: No duplicate primes returned

## Running Tests

### Run All Tests

```bash
python -m pytest test_prime_finder.py -v
```

Output:

```
test_prime_finder.py::TestIsPrime::test_composite_numbers PASSED
test_prime_finder.py::TestIsPrime::test_even_numbers PASSED
test_prime_finder.py::TestIsPrime::test_large_composite PASSED
test_prime_finder.py::TestIsPrime::test_large_prime PASSED
test_prime_finder.py::TestIsPrime::test_negative_numbers PASSED
test_prime_finder.py::TestIsPrime::test_small_primes PASSED
test_prime_finder.py::TestIsPrime::test_two_is_prime PASSED
test_prime_finder.py::TestIsPrime::test_zero_and_one PASSED
test_prime_finder.py::TestFindPrimesUpTo::test_all_results_are_prime PASSED
test_prime_finder.py::TestFindPrimesUpTo::test_no_composites_returned PASSED
test_prime_finder.py::TestFindPrimesUpTo::test_primes_up_to_one PASSED
test_prime_finder.py::TestFindPrimesUpTo::test_primes_up_to_ten PASSED
test_prime_finder.py::TestFindPrimesUpTo::test_primes_up_to_thirty PASSED
test_prime_finder.py::TestFindPrimesUpTo::test_primes_up_to_two PASSED
test_prime_finder.py::TestFindPrimesUpTo::test_primes_up_to_two_is_inclusive PASSED
test_prime_finder.py::TestFindPrimesUpTo::test_primes_up_to_zero PASSED
test_prime_finder.py::TestFindNPrimes::test_all_results_are_prime PASSED
test_prime_finder.py::TestFindNPrimes::test_correct_count_returned PASSED
test_prime_finder.py::TestFindNPrimes::test_find_five_primes PASSED
test_prime_finder.py::TestFindNPrimes::test_find_one_prime PASSED
test_prime_finder.py::TestFindNPrimes::test_find_ten_primes PASSED
test_prime_finder.py::TestFindNPrimes::test_find_zero_primes PASSED
test_prime_finder.py::TestFindNPrimes::test_no_duplicates PASSED
test_prime_finder.py::TestFindNPrimes::test_returns_first_primes_in_order PASSED

24 passed in 0.03s
```

### Run Specific Test Class

```bash
python -m pytest test_prime_finder.py::TestIsPrime -v
```

### Run Specific Test

```bash
python -m pytest test_prime_finder.py::TestIsPrime::test_small_primes -v
```

### Run Using unittest

```bash
python -m unittest test_prime_finder
```

## Code Quality

### Linting

All code is linted with pylint and flake8:

```bash
# Python linting
python -m pylint prime_finder.py test_prime_finder.py
python -m flake8 prime_finder.py test_prime_finder.py

# Markdown linting
python -m mdformat --check README.md TESTING.md
```

**Status**: All checks passing

- `prime_finder.py`: pylint 10.0/10, flake8 clean
- `test_prime_finder.py`: pylint 10.0/10, flake8 clean
- Documentation: mdformat compliant (0 warnings)

## Test Coverage

The test suite covers:

- **Input validation**: Negative numbers, edge cases (0, 1, 2)
- **Correctness**: Known prime and composite numbers, multiple ranges
- **Boundary conditions**: Empty results, inclusive/exclusive limits
- **Output properties**: Order, uniqueness, count accuracy
- **Integration**: Cross-validation using multiple functions

Total coverage includes all three public functions with comprehensive scenarios.

## Requirements

- Python 3.6+
- pytest (for running tests)
- pylint, flake8 (for code quality)
- mdformat (for documentation)

## Future Improvements

- Add performance benchmarks for large numbers
- Add hypothesis-based property testing
- Increase coverage for edge cases with very large primes
