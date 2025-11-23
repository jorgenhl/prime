#!/usr/bin/env python3
"""Prime number finder with multiprocessing parallelization."""

import math
import sys
from multiprocessing import Pool, cpu_count


def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def is_prime_with_num(args):
    """Wrapper for is_prime that returns (num, is_prime_bool)."""
    num, _ = args
    return (num, is_prime(num))


def find_primes_up_to_parallel(limit, num_processes=None):
    """Find all primes up to limit using multiprocessing.

    Args:
        limit: Upper bound (inclusive)
        num_processes: Number of processes (None = auto-detect CPU count)

    Returns:
        List of primes up to limit
    """
    if num_processes is None:
        num_processes = cpu_count()

    if limit < 2:
        return []

    # Create list of (number, placeholder) tuples for workers
    numbers = list(range(2, limit + 1))
    work_items = [(n, None) for n in numbers]

    # Use Pool to check primality in parallel
    with Pool(processes=num_processes) as pool:
        results = pool.map(is_prime_with_num, work_items)

    # Filter to only primes
    primes = [num for num, is_p in results if is_p]
    return primes


def find_n_primes_parallel(count, num_processes=None):
    """Find the first N prime numbers using multiprocessing.

    Strategy: Use binary search to estimate upper bound, then filter.

    Args:
        count: Number of primes to find
        num_processes: Number of processes (None = auto-detect CPU count)

    Returns:
        List of first N primes
    """
    if num_processes is None:
        num_processes = cpu_count()

    if count == 0:
        return []
    if count == 1:
        return [2]

    # Estimate upper bound for Nth prime using prime number theorem
    # Nth prime ~ N * ln(N)
    if count < 6:
        upper_bound = 15
    else:
        ln_n = math.log(count)
        upper_bound = int(count * (ln_n + math.log(ln_n)))

    # Keep expanding until we have enough primes
    while True:
        primes = find_primes_up_to_parallel(upper_bound, num_processes)
        if len(primes) >= count:
            return primes[:count]
        # Expand search range
        upper_bound = int(upper_bound * 1.5)


def parse_arguments():
    """Parse command line arguments.

    Returns:
        Tuple of (command, value, num_processes)
    """
    num_cpus = cpu_count()
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python prime_finder_parallel.py <number> [--processes N]")
        print("    Check if a number is prime")
        print("  python prime_finder_parallel.py -u <limit> [--processes N]")
        print("    Find all primes up to limit")
        print("  python prime_finder_parallel.py -n <count> [--processes N]")
        print("    Find the first N primes")
        print(f"\n  [--processes N]  "
              f"Number of processes (default: {num_cpus})")
        sys.exit(1)

    # Parse --processes argument if present
    num_processes = None
    if "--processes" in sys.argv:
        idx = sys.argv.index("--processes")
        if idx + 1 < len(sys.argv):
            try:
                num_processes = int(sys.argv[idx + 1])
            except ValueError:
                print("Error: --processes requires an integer argument")
                sys.exit(1)
        # Remove from sys.argv for easier parsing
        sys.argv.pop(idx)
        sys.argv.pop(idx)

    command = sys.argv[1]
    value = int(sys.argv[2]) if len(sys.argv) > 2 else None
    return command, value, num_processes


def execute_command(command, value, num_processes):
    """Execute the prime finder command.

    Args:
        command: Command type ("-u", "-n", or number)
        value: Value for the command
        num_processes: Number of processes to use
    """
    if command == "-u":
        if value is None:
            print("Error: -u requires a limit argument")
            sys.exit(1)
        primes = find_primes_up_to_parallel(value, num_processes)
        print(f"Primes up to {value}: {primes}")
        print(f"Total: {len(primes)} primes")

    elif command == "-n":
        if value is None:
            print("Error: -n requires a count argument")
            sys.exit(1)
        primes = find_n_primes_parallel(value, num_processes)
        print(f"First {value} primes: {primes}")

    else:
        num = int(command)
        if is_prime(num):
            print(f"{num} is prime")
        else:
            print(f"{num} is not prime")


def main():
    """Main entry point for the parallel prime finder script."""
    command, value, num_processes = parse_arguments()
    execute_command(command, value, num_processes)


if __name__ == "__main__":
    main()
