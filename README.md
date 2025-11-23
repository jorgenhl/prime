# Prime Finder

A simple Python script to find and check prime numbers with multiple search options.

## Features

- **Check if a number is prime**: Verify whether a single number is prime
- **Find all primes up to a limit**: Generate all prime numbers up to a specified value
- **Find the first N primes**: Generate the first N prime numbers

## Usage

```bash
# Check if a number is prime
python prime_finder.py <number>

# Find all primes up to a limit
python prime_finder.py -u <limit>

# Find the first N primes
python prime_finder.py -n <count>
```

### Examples

```bash
# Check if 17 is prime
python prime_finder.py 17
# Output: 17 is prime

# Find all primes up to 30
python prime_finder.py -u 30
# Output: Primes up to 30: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
# Total: 10 primes

# Find the first 10 primes
python prime_finder.py -n 10
# Output: First 10 primes: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

## Requirements

- Python 3.6+

## Algorithm

The script uses trial division with √n optimization for efficient prime checking.
