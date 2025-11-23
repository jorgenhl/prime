#!/usr/bin/env python3
"""Parallel benchmark for prime finder using multiprocessing."""

import json
import os
import time
from multiprocessing import cpu_count

from src.prime_finder_parallel import find_n_primes_parallel

CHECKPOINT_FILE = "benchmark_parallel_checkpoint.json"


def save_checkpoint(count, elapsed_time, num_processes):
    """Save benchmark progress to checkpoint file."""
    checkpoint = {
        "count": count,
        "elapsed_time": elapsed_time,
        "num_processes": num_processes,
        "timestamp": time.time()
    }
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f)


def load_checkpoint():
    """Load benchmark progress from checkpoint file if it exists."""
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                checkpoint = json.load(f)
            return checkpoint
        except (json.JSONDecodeError, IOError):
            return None
    return None


def main():
    """Run parallel prime finding for 5 minutes and report progress."""
    num_processes = cpu_count()
    checkpoint = load_checkpoint()
    start_count = checkpoint["count"] if checkpoint else 0
    start_time = time.time()
    batch_size = 1000

    if checkpoint:
        num_processes = checkpoint.get("num_processes", num_processes)
        print("Resuming parallel benchmark from checkpoint...")
        print(f"Previous run: {checkpoint['count']:,} primes in "
              f"{checkpoint['elapsed_time']:.1f}s using "
              f"{checkpoint['num_processes']} processes")
        print("=" * 60)
    else:
        print("Starting 5-minute parallel prime finder benchmark...")
        print(f"Using {num_processes} processes")
        print("=" * 60)

    count = start_count
    while time.time() - start_time < 300:  # 300 seconds = 5 minutes
        count += batch_size
        primes = find_n_primes_parallel(count, num_processes)
        elapsed = time.time() - start_time
        save_checkpoint(count, elapsed, num_processes)
        print(f"[{elapsed:6.1f}s] Found {count:7d} primes. "
              f"Largest: {primes[-1]:7d}")

    elapsed = time.time() - start_time
    print("=" * 60)
    print(f"\nCompleted in {elapsed:.1f} seconds")
    print(f"Total primes found: {len(primes):,}")
    print(f"Largest prime: {primes[-1]:,}")
    print(f"Average rate: {len(primes) / elapsed:.1f} primes/second")
    print(f"Processes used: {num_processes}")
    print(f"\nFirst 10 primes: {primes[:10]}")
    print(f"Last 10 primes: {primes[-10:]}")

    # Clean up checkpoint on successful completion
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)
        print("\nCheckpoint cleared (benchmark completed successfully)")


if __name__ == "__main__":
    main()
