#!/usr/bin/env python3
"""Benchmark prime finder performance over 5 minutes with checkpointing."""

import json
import os
import time

from src.prime_finder import find_n_primes

CHECKPOINT_FILE = "benchmark_checkpoint.json"


def save_checkpoint(count, elapsed_time):
    """Save benchmark progress to checkpoint file."""
    checkpoint = {
        "count": count,
        "elapsed_time": elapsed_time,
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
    """Run prime finding for 5 minutes and report progress."""
    checkpoint = load_checkpoint()
    start_count = checkpoint["count"] if checkpoint else 0
    start_time = time.time()
    batch_size = 1000

    if checkpoint:
        print("Resuming benchmark from checkpoint...")
        print(f"Previous run: {checkpoint['count']:,} primes in "
              f"{checkpoint['elapsed_time']:.1f}s")
        print("=" * 60)
    else:
        print("Starting 5-minute prime finder benchmark...")
        print("=" * 60)

    count = start_count
    while time.time() - start_time < 300:  # 300 seconds = 5 minutes
        count += batch_size
        primes = find_n_primes(count)
        elapsed = time.time() - start_time
        save_checkpoint(count, elapsed)
        print(f"[{elapsed:6.1f}s] Found {count:7d} primes. "
              f"Largest: {primes[-1]:7d}")

    elapsed = time.time() - start_time
    print("=" * 60)
    print(f"\nCompleted in {elapsed:.1f} seconds")
    print(f"Total primes found: {len(primes):,}")
    print(f"Largest prime: {primes[-1]:,}")
    print(f"Average rate: {len(primes) / elapsed:.1f} primes/second")
    print(f"\nFirst 10 primes: {primes[:10]}")
    print(f"Last 10 primes: {primes[-10:]}")

    # Clean up checkpoint on successful completion
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)
        print("\nCheckpoint cleared (benchmark completed successfully)")


if __name__ == "__main__":
    main()
