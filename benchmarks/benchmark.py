#!/usr/bin/env python3
"""Benchmark prime finder performance with checkpointing."""

import argparse
import json
import os
import sys
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
    """Run prime finding with configurable options."""
    parser = argparse.ArgumentParser(
        description="Benchmark prime finder with checkpointing support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m benchmark.benchmark
    Run for 5 minutes (default), resume from checkpoint if available

  python -m benchmark.benchmark --time 60
    Run for 60 seconds, resume from checkpoint if available

  python -m benchmark.benchmark --count 100000
    Find the first 100,000 primes

  python -m benchmark.benchmark --start 50000
    Start calculating from 50,000 primes (no checkpoint)

  python -m benchmark.benchmark --count 100000 --resume
    Find 100,000 primes, resume from checkpoint if available
        """
    )
    parser.add_argument(
        "--time",
        type=int,
        default=300,
        help="Run for N seconds (default: 300). Incompatible with --count."
    )
    parser.add_argument(
        "--count",
        type=int,
        help="Find N primes instead of running for a duration."
    )
    parser.add_argument(
        "--start",
        type=int,
        default=0,
        help="Start from N primes (ignores checkpoint, default: 0)"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        default=True,
        help="Resume from checkpoint file if available (default: True)"
    )
    parser.add_argument(
        "--no-resume",
        dest="resume",
        action="store_false",
        help="Do not resume from checkpoint, start fresh"
    )

    args = parser.parse_args()

    # Validate arguments
    if args.count and args.time != 300:
        print("Error: Cannot use both --time and --count options together.")
        sys.exit(1)

    # Determine start state
    checkpoint = None
    if args.resume and args.start == 0:
        checkpoint = load_checkpoint()

    start_count = checkpoint["count"] if checkpoint else args.start
    start_elapsed = checkpoint["elapsed_time"] if checkpoint else 0
    start_time = time.time() - start_elapsed
    batch_size = 1000

    # Print mode
    if args.count:
        print(f"Finding the first {args.count:,} primes...")
    else:
        print(f"Running benchmark for {args.time} seconds...")

    if checkpoint and args.resume:
        print(f"Resuming from checkpoint: {checkpoint['count']:,} primes in "
              f"{checkpoint['elapsed_time']:.1f}s")
    elif args.start > 0:
        print(f"Starting from {args.start:,} primes...")

    print("=" * 60)

    count = start_count
    mode = "count" if args.count else "time"

    while True:
        count += batch_size

        # Check if we should stop
        if mode == "count" and count >= args.count:
            count = args.count

        primes = find_n_primes(count)
        elapsed = time.time() - start_time

        if mode == "count":
            print(f"[{elapsed:6.1f}s] Found {count:7d} primes. "
                  f"Largest: {primes[-1]:7d}")
            if count >= args.count:
                break
        else:
            save_checkpoint(count, elapsed)
            print(f"[{elapsed:6.1f}s] Found {count:7d} primes. "
                  f"Largest: {primes[-1]:7d}")
            if elapsed >= args.time:
                break

    elapsed = time.time() - start_time
    print("=" * 60)
    print(f"\nCompleted in {elapsed:.1f} seconds")
    print(f"Total primes found: {len(primes):,}")
    print(f"Largest prime: {primes[-1]:,}")
    print(f"Average rate: {len(primes) / elapsed:.1f} primes/second")
    print(f"\nFirst 10 primes: {primes[:10]}")
    print(f"Last 10 primes: {primes[-10:]}")

    # Clean up checkpoint on successful completion (only for time-based mode)
    if mode == "time" and os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)
        print("\nCheckpoint cleared (benchmark completed successfully)")


if __name__ == "__main__":
    main()
