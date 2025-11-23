#!/usr/bin/env python3
"""Prime finder with checkpointing support for HPC clusters."""

import json
import os
import sys
import time

from src.prime_finder import find_n_primes

CHECKPOINT_FILE = "prime_checkpoint.json"


def save_checkpoint(count, elapsed_time):
    """Save current progress to checkpoint file."""
    checkpoint = {"count": count, "elapsed_time": elapsed_time,
                  "timestamp": time.time()}
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f)
    print(f"[Checkpoint] Saved: {count} primes at {elapsed_time:.1f}s")


def load_checkpoint():
    """Load progress from checkpoint file if it exists."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
            checkpoint = json.load(f)
        print(f"[Recovery] Resuming from checkpoint: "
              f"{checkpoint['count']} primes at "
              f"{checkpoint['elapsed_time']:.1f}s")
        return checkpoint
    return None


def find_primes_with_checkpoint(target_count, checkpoint_interval=1000,
                                time_limit=None):
    """Find primes with periodic checkpointing."""
    checkpoint = load_checkpoint()
    start_count = checkpoint["count"] if checkpoint else 0
    start_time = time.time()

    print(f"Finding {target_count} primes (starting from {start_count})")
    print("=" * 60)

    count = start_count
    while count < target_count:
        if time_limit and (time.time() - start_time) > time_limit:
            elapsed = time.time() - start_time
            save_checkpoint(count, elapsed)
            print(f"[Timeout] Reached time limit. Checkpointed at "
                  f"{count} primes.")
            sys.exit(0)

        count += checkpoint_interval
        count = min(count, target_count)

        primes = find_n_primes(count)
        elapsed = time.time() - start_time
        save_checkpoint(count, elapsed)

        print(f"[{elapsed:6.1f}s] Found {count:7d} primes. "
              f"Largest: {primes[-1]:7d}")

    elapsed = time.time() - start_time
    print("=" * 60)
    print(f"Completed in {elapsed:.1f} seconds")
    print(f"Total primes found: {len(primes):,}")
    print(f"Largest prime: {primes[-1]:,}")

    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prime_finder_checkpoint.py <count> "
              "[max_time_seconds]")
        sys.exit(1)

    target = int(sys.argv[1])
    max_time_limit = int(sys.argv[2]) if len(sys.argv) > 2 else None

    find_primes_with_checkpoint(target, time_limit=max_time_limit)
