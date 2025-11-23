#!/usr/bin/env python3
"""Benchmark prime finder performance over 5 minutes."""

import time
from src.prime_finder import find_n_primes


def main():
    """Run prime finding for 5 minutes and report progress."""
    start = time.time()
    count = 0
    batch_size = 1000

    print("Starting 5-minute prime finder benchmark...")
    print("=" * 60)

    while time.time() - start < 300:  # 300 seconds = 5 minutes
        count += batch_size
        primes = find_n_primes(count)
        elapsed = time.time() - start
        print(f"[{elapsed:6.1f}s] Found {count:7d} primes. "
              f"Largest: {primes[-1]:7d}")

    elapsed = time.time() - start
    print("=" * 60)
    print(f"\nCompleted in {elapsed:.1f} seconds")
    print(f"Total primes found: {len(primes):,}")
    print(f"Largest prime: {primes[-1]:,}")
    print(f"Average rate: {len(primes) / elapsed:.1f} primes/second")
    print(f"\nFirst 10 primes: {primes[:10]}")
    print(f"Last 10 primes: {primes[-10:]}")


if __name__ == "__main__":
    main()
