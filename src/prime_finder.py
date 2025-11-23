#!/usr/bin/env python3
"""Prime number finder with multiple search options."""

import sys


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


def find_primes_up_to(limit):
    """Find all prime numbers up to a given limit."""
    return [n for n in range(2, limit + 1) if is_prime(n)]


def find_n_primes(count):
    """Find the first N prime numbers."""
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes


def main():
    """Main entry point for the prime finder script."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python prime_finder.py <number>")
        print("    Check if a number is prime")
        print("  python prime_finder.py -u <limit>")
        print("    Find all primes up to limit")
        print("  python prime_finder.py -n <count>")
        print("    Find the first N primes")
        sys.exit(1)

    if sys.argv[1] == "-u":
        if len(sys.argv) < 3:
            print("Error: -u requires a limit argument")
            sys.exit(1)
        limit = int(sys.argv[2])
        primes = find_primes_up_to(limit)
        print(f"Primes up to {limit}: {primes}")
        print(f"Total: {len(primes)} primes")

    elif sys.argv[1] == "-n":
        if len(sys.argv) < 3:
            print("Error: -n requires a count argument")
            sys.exit(1)
        count = int(sys.argv[2])
        primes = find_n_primes(count)
        print(f"First {count} primes: {primes}")

    else:
        num = int(sys.argv[1])
        if is_prime(num):
            print(f"{num} is prime")
        else:
            print(f"{num} is not prime")


if __name__ == "__main__":
    main()
