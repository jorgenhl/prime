# Checkpointing Guide for HPC Clusters

## Overview

Checkpointing is a fault-tolerance strategy for long-running jobs on SLURM-managed HPC clusters. It
allows jobs to save their computational state periodically, enabling recovery from node failures,
time limit expiration, or preemption without losing progress.

## Why Checkpointing?

On computation clusters, jobs can be interrupted by:

- **Time limits**: Jobs reaching their `--time` allocation
- **Node failures**: Hardware failures on compute nodes
- **Preemption**: Higher-priority jobs requiring resources
- **Maintenance**: Scheduled cluster maintenance

**Without checkpointing**: All progress is lost, computation restarts from scratch (wasted
resources).

**With checkpointing**: Job resumes from the last saved state, minimizing wasted compute time and
improving cluster resilience.

## Checkpointing Approaches

### 1. Application-Level Checkpointing (Recommended)

The application itself saves and restores its state.

**Pros:**

- Most efficient (smallest checkpoint files)
- Fastest restart
- Fine-grained control over what's saved

**Cons:**

- Requires application support
- Needs code modifications

**Best for:** Python simulations, machine learning, custom applications

### 2. User-Level Checkpointing

You integrate checkpointing into your job script or code using libraries.

**Pros:**

- Works with many applications
- Moderate control
- No system-level dependencies

**Cons:**

- Manual implementation required
- More code overhead

**Best for:** Custom Python scripts, research code, flexible workflows

### 3. System-Level Checkpointing

Captures entire process state (memory, file handles, registers).

**Pros:**

- Works on any program
- No application modification needed

**Cons:**

- Large checkpoint files
- Slower save/restore
- More storage required

**Best for:** Legacy binaries, compiled code without source

## Common Tools

| Tool | Type | Best For | Notes |
|------|------|----------|-------|
| **DMTCP** | System-level | MPI/OpenMP jobs | Flexible, active development |
| **BLCR** | System-level | SLURM integration | Tightly integrated with SLURM |
| **CRIU** | System-level | Containerized workloads | Modern, good for containers |
| **Custom Python** | Application-level | Python scripts | Easiest for your prime finder |

## Implementing Checkpointing for the Prime Finder

### Approach: Application-Level Checkpointing with Python

The prime finder script can be enhanced with checkpointing by:

1. **Saving progress** after finding each batch of primes
1. **Loading state** on restart
1. **Resuming computation** from the last checkpoint

### Modified Script with Checkpointing

```python
#!/usr/bin/env python3
"""Prime finder with checkpointing support for HPC clusters."""

import json
import os
import sys
import time
from prime_finder import find_n_primes


CHECKPOINT_FILE = "prime_checkpoint.json"


def save_checkpoint(count, elapsed_time):
    """Save current progress to checkpoint file."""
    checkpoint = {
        "count": count,
        "elapsed_time": elapsed_time,
        "timestamp": time.time()
    }
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(checkpoint, f)
    print(f"[Checkpoint] Saved: {count} primes at {elapsed_time:.1f}s")


def load_checkpoint():
    """Load progress from checkpoint file if it exists."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            checkpoint = json.load(f)
        print(f"[Recovery] Resuming from checkpoint: "
              f"{checkpoint['count']} primes at {checkpoint['elapsed_time']:.1f}s")
        return checkpoint
    return None


def find_primes_with_checkpoint(target_count, checkpoint_interval=1000,
                                max_time=None):
    """Find primes with periodic checkpointing."""
    # Load previous progress if available
    checkpoint = load_checkpoint()
    start_count = checkpoint["count"] if checkpoint else 0
    start_time = time.time()

    print(f"Finding {target_count} primes (starting from {start_count})")
    print("=" * 60)

    count = start_count
    while count < target_count:
        # Check time limit if specified
        if max_time and (time.time() - start_time) > max_time:
            elapsed = time.time() - start_time
            save_checkpoint(count, elapsed)
            print(f"[Timeout] Reached time limit. Checkpointed at {count} primes.")
            sys.exit(0)

        # Increment by checkpoint interval
        count += checkpoint_interval
        if count > target_count:
            count = target_count

        # Find primes and save checkpoint
        primes = find_n_primes(count)
        elapsed = time.time() - start_time
        save_checkpoint(count, elapsed)

        print(f"[{elapsed:6.1f}s] Found {count:7d} primes. "
              f"Largest: {primes[-1]:7d}")

    # Final results
    elapsed = time.time() - start_time
    print("=" * 60)
    print(f"Completed in {elapsed:.1f} seconds")
    print(f"Total primes found: {len(primes):,}")
    print(f"Largest prime: {primes[-1]:,}")

    # Clean up checkpoint file on successful completion
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prime_finder_checkpoint.py <count> [max_time_seconds]")
        sys.exit(1)

    target = int(sys.argv[1])
    max_time = int(sys.argv[2]) if len(sys.argv) > 2 else None

    find_primes_with_checkpoint(target, max_time=max_time)
```

### SLURM Job Script Example

```bash
#!/bin/bash
#SBATCH --job-name=prime_finder
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:05:00          # 5 minutes per job
#SBATCH --requeue                # Auto-requeue on timeout
#SBATCH --output=prime_%j.log

# Set checkpoint file to persist across jobs
export CHECKPOINT_DIR="$HOME/prime_checkpoints"
mkdir -p $CHECKPOINT_DIR
cd $CHECKPOINT_DIR

# Load python environment
module load python/3.10

# Run with checkpointing
# Time limit is 5 minutes SLURM time minus 30s safety buffer
python /path/to/prime_finder_checkpoint.py 1000000 300

# Job will checkpoint at 5 minutes and SLURM will requeue it
# On next submission, it resumes from saved checkpoint
```

### How It Works

1. **First submission**:

   - Job starts finding primes from count 0
   - Every 1,000 primes, saves progress to `prime_checkpoint.json`
   - After 4.5 minutes, reaches SLURM time limit

1. **Checkpoint saved**:

   - Current count and elapsed time saved to file
   - Job exits gracefully with status 0

1. **Auto-requeue** (via `#SBATCH --requeue`):

   - SLURM automatically resubmits the job
   - Job script runs again

1. **Resume**:

   - Script loads `prime_checkpoint.json`
   - Resumes from last saved count
   - Continues finding primes

## Implementation Steps

### Step 1: Create Checkpointing Wrapper

Create `prime_finder_checkpoint.py` with the code above.

### Step 2: Test Locally

```bash
# Simulate a time-limited run
python prime_finder_checkpoint.py 10000 5  # Find 10k primes with 5s limit

# Check checkpoint file was created
cat prime_checkpoint.json

# Resume from checkpoint
python prime_finder_checkpoint.py 10000 5  # Should resume from saved state
```

### Step 3: Submit to SLURM

```bash
sbatch prime_job.sh
```

Monitor with:

```bash
squeue -u $USER
tail -f prime_*.log
```

## Best Practices

### Checkpoint Frequency

Balance between:

- **Too frequent**: Overhead from saving, slower progress
- **Too infrequent**: Large loss if failure occurs

For prime finder: **Every 1,000 primes** is reasonable (< 1 second overhead).

### Storage

- Store checkpoints on **persistent shared storage** (NFS, Lustre)
- **Not** on local node storage (lost on node failure)
- Include unique job ID in checkpoint filename for parallel jobs:

```python
CHECKPOINT_FILE = f"prime_checkpoint_{os.environ.get('SLURM_JOB_ID', 'local')}.json"
```

### Safety

```python
# Atomic write - avoid corrupting checkpoint
def save_checkpoint(count, elapsed_time):
    checkpoint = {"count": count, "elapsed_time": elapsed_time}
    
    # Write to temporary file first
    temp_file = CHECKPOINT_FILE + ".tmp"
    with open(temp_file, "w") as f:
        json.dump(checkpoint, f)
    
    # Atomic rename
    os.replace(temp_file, CHECKPOINT_FILE)
```

### Clean Up

```python
# Delete checkpoint on successful completion
if job_completed_successfully:
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)
```

## Monitoring and Debugging

### Check Job Status

```bash
sinfo                    # Cluster status
squeue -u $USER         # Your jobs
sstat -j <job_id>       # Resource usage
sacct -j <job_id>       # Job history
```

### View Checkpoint File

```bash
cat prime_checkpoint.json
```

### Debug Requeue Chain

```bash
# See all subjobs in the requeue chain
scontrol show job <initial_job_id>

# Check timestamps to see requeue pattern
sacct --format=JobID,JobName,State,Start,End
```

## Advanced Topics

### Parallel Prime Finding with Checkpointing

For MPI or multi-process jobs:

```python
# Each process saves its own checkpoint
checkpoint_file = f"prime_checkpoint_{rank}.json"

# Coordinator process saves aggregate progress
if rank == 0:
    aggregate_checkpoint = {"total": total_primes, "ranges_completed": ranges}
    save_checkpoint(aggregate_checkpoint)
```

### Incremental Computation

Instead of recalculating all primes from 0:

```python
# Load checkpoint
checkpoint = load_checkpoint()

# Find only new primes from last count
primes = find_n_primes_from(checkpoint["count"], target_count)

# More efficient if computation is expensive
```

### Containerized Checkpointing

For Docker/Singularity jobs with CRIU:

```bash
# In SLURM script
srun -n 1 criu dump -t <pid> -D <checkpoint_dir>
# ... later ...
srun -n 1 criu restore -D <checkpoint_dir>
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Checkpoint not saving | File permissions | Check write access to `CHECKPOINT_DIR` |
| Job not requeuing | Missing `--requeue` flag | Add to `#SBATCH` header |
| Large checkpoint files | Saving full state | Optimize to save only essential data |
| Slow restart | I/O bottleneck | Use local SSD + copy to shared storage |

## References

- [SLURM Checkpoint/Restart Documentation](https://slurm.schedmc.com)
- [DMTCP: Distributed MultiThreaded Checkpointing](https://dmtcp.sourceforge.io)
- [BLCR: Berkeley Lab Checkpoint/Restart](https://ftg.lbl.gov/CheckpointRestart)
- [CRIU: Checkpoint/Restore in Userspace](https://criu.org)

## Summary

For your prime finder script:

1. **Use application-level checkpointing** (simplest, no cluster dependencies)
1. **Save/load JSON with prime count** (minimal overhead)
1. **Set `--requeue` in SLURM script** (automatic resumption)
1. **Test locally first** before submitting to cluster
1. **Monitor job history** to understand requeue patterns
