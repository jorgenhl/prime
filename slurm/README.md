# SLURM Job Scripts

This folder contains SLURM job scripts for running the prime finder on HPC clusters managed by
SLURM.

## Quick Start

```bash
# Submit basic job to $SCRATCH
sbatch prime_finder.slurm

# Submit with checkpointing (auto-requeue)
sbatch prime_finder_checkpoint.slurm

# Monitor jobs
squeue -u $USER
tail -f prime_ckpt_*.log

# View checkpoint progress
cat $SCRATCH/prime_finder_main/benchmark_checkpoint.json
```

## Job Scripts

### `prime_finder.slurm`

Basic job script for finding primes with checkpointing.

**Configuration:**

- Time: 10 minutes
- CPUs: 4
- Memory: 4 GB
- Nodes: 1
- **Working directory**: `$SCRATCH/prime_finder_$SLURM_JOB_ID/`

**Features:**

- Automatic checkpointing to `$SCRATCH`
- Creates job-specific subdirectory for isolation
- Resumes from checkpoint if interrupted
- Available on all compute nodes

**Usage:**

```bash
sbatch prime_finder.slurm
```

**Output:**

- `prime_<job_id>.log` - Standard output
- `prime_<job_id>.err` - Standard error
- `$SCRATCH/prime_finder_<job_id>/benchmark_checkpoint.json` - Checkpoint state

**Best for:**

- Quick tests
- Single 10-minute runs
- Development and debugging

### `prime_finder_checkpoint.slurm`

Job script with checkpointing support for long-running jobs.

**Configuration:**

- Time: 5 minutes
- CPUs: 4
- Memory: 4 GB
- Nodes: 1
- **Auto-requeue: Enabled**
- **Working directory**: `$SCRATCH/prime_finder_main/`

**Key Features:**

- Automatically saves progress to `$SCRATCH/prime_finder_main/`
- Resumes from last checkpoint on timeout
- Uses same directory across requeues for persistent progress
- Shared across all compute nodes via `$SCRATCH`

**Usage:**

```bash
sbatch prime_finder_checkpoint.slurm
```

**Output:**

- `prime_ckpt_<job_id>.log` - Standard output
- `prime_ckpt_<job_id>.err` - Standard error
- `$SCRATCH/prime_finder_main/benchmark_checkpoint.json` - Checkpoint state

**Best for:**

- Long-running jobs exceeding time limits
- Finding very large prime numbers
- Fault tolerance on unstable clusters
- Jobs requiring multiple requeue cycles

## Monitoring Jobs

### View All Jobs

```bash
squeue -u $USER
```

Shows job ID, name, status, time remaining, and more.

### View Specific Job

```bash
squeue -j <job_id>
scontrol show job <job_id>
```

Get detailed information about a specific job.

### View Job History

```bash
sacct -u $USER
sacct -j <job_id>
```

Show completed and running job information.

### Stream Output

```bash
tail -f prime_*.log
```

Watch job progress in real-time.

## Managing Jobs

### Cancel Job

```bash
scancel <job_id>
```

Stop a running or queued job.

### Cancel All Jobs

```bash
scancel -u $USER
```

Stop all your jobs.

### Hold Job

```bash
scontrol hold <job_id>
```

Prevent a job from running while in queue.

### Release Job

```bash
scontrol release <job_id>
```

Allow a held job to run.

## Checkpointing Details

### How It Works

1. **Job starts** - Loads checkpoint if it exists, otherwise starts from 0
1. **Periodic saves** - Every 1,000 primes, progress is saved
1. **Timeout approach** - Job completes after 5 minutes
1. **Auto-requeue** - SLURM resubmits with `--requeue` flag
1. **Resume** - Next job loads checkpoint and continues

### Checkpoint Location

- **Basic job**: `$SCRATCH/prime_finder_<job_id>/benchmark_checkpoint.json`
- **Checkpoint job**: `$SCRATCH/prime_finder_main/benchmark_checkpoint.json`

Benefits of `$SCRATCH`:

- Available on all compute nodes
- Automatic cleanup by cluster (periodic purge)
- Faster I/O than home directory
- No quota limits

### Checkpoint File Format

```json
{
  "count": 100000,
  "elapsed_time": 245.3,
  "timestamp": 1700729400.5
}
```

- **count**: Number of primes found so far
- **elapsed_time**: Seconds elapsed (across all job submissions)
- **timestamp**: Unix timestamp of checkpoint

### Viewing Checkpoints

```bash
# Check if checkpoint exists (basic job)
ls -lh $SCRATCH/prime_finder_*/benchmark_checkpoint.json

# View checkpoint for auto-requeue job
cat $SCRATCH/prime_finder_main/benchmark_checkpoint.json

# Watch progress live
watch -n 5 'cat $SCRATCH/prime_finder_main/benchmark_checkpoint.json | python -m json.tool'
```

### Tracking Requeue Chain

When a job requeues, SLURM tracks it as a chain:

```bash
# View all subjobs in requeue chain
scontrol show job <initial_job_id>

# View formatted job history with timestamps
sacct --format=JobID,JobName,State,Start,End,Elapsed
```

### Cleaning Up Checkpoints

```bash
# Remove checkpoint for basic job
rm $SCRATCH/prime_finder_<job_id>/benchmark_checkpoint.json

# Remove all basic job checkpoints
rm -rf $SCRATCH/prime_finder_[0-9]*/

# Remove auto-requeue checkpoint (careful - loses progress!)
rm $SCRATCH/prime_finder_main/benchmark_checkpoint.json

# Remove all checkpoints
rm -rf $SCRATCH/prime_finder_*/
```

## Customizing Scripts

Both scripts use the benchmark's built-in checkpointing. To modify behavior:

### Increase Memory

```bash
#SBATCH --mem=8G  # 8 GB instead of 4 GB
```

### Use More CPUs

```bash
#SBATCH --cpus-per-task=8
```

(Note: Prime finder is single-threaded, so extra CPUs help other cluster tasks)

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Job won't start | Queue full | Wait or increase priority |
| Checkpoint not saving | No write access to `$SCRATCH` | Check `$SCRATCH` permissions |
| Job not requeuing | Missing `--requeue` flag | Add `#SBATCH --requeue` to script |
| Lost progress | Checkpoint deleted | Don't delete unless intentional |
| Slow progress | I/O bottleneck | Check `$SCRATCH` performance |
| Module not found | Python not loaded | Check `module load python/3.10` |
| Permission denied | `$SCRATCH` access | Verify cluster `$SCRATCH` setup |

## Example Workflows

### Find 10 Million Primes with Checkpointing

```bash
# Edit checkpoint script to find 10M primes
# Then submit:
sbatch prime_finder_checkpoint.slurm

# Monitor progress
watch -n 10 'cat ~/prime_checkpoints/prime_checkpoint.json'

# After job completes, check results
tail -100 prime_ckpt_*.log
```

### Run Multiple Experiments in Parallel

```bash
# Each in separate directory
mkdir exp1 exp2 exp3
cd exp1 && sbatch ../slurm/prime_finder_checkpoint.slurm
cd ../exp2 && sbatch ../slurm/prime_finder_checkpoint.slurm
cd ../exp3 && sbatch ../slurm/prime_finder_checkpoint.slurm

# Monitor all
squeue -u $USER
```

### Profile Performance

```bash
# Run with timing
/usr/bin/time -v sbatch prime_finder.slurm

# View resource usage
sstat -j <job_id> --format=AveCPU,AveVMSize,MaxRSS
```

## SLURM Command Reference

```bash
# Information
sinfo                     # Cluster status
squeue                    # All jobs
squeue -u $USER          # Your jobs
sacct                     # Job history
module avail             # Available modules
module list              # Loaded modules

# Submission
sbatch script.slurm      # Submit job
srun command             # Run command in parallel
salloc                   # Allocate resources interactively

# Management
scancel <job_id>         # Cancel job
scontrol hold <job_id>   # Hold job
scontrol release <job_id> # Release job
scontrol update ...      # Modify running job

# Monitoring
sstat -j <job_id>       # Running job stats
sacct -j <job_id>       # Completed job info
tail -f output.log       # Stream output
```

## References

- [Official SLURM Documentation](https://slurm.schedmd.com/)
- [SLURM sbatch Manual](https://slurm.schedmd.com/sbatch.html)
- [SLURM squeue Manual](https://slurm.schedmd.com/squeue.html)
- [Prime Finder Checkpointing Guide](../docs/CHECKPOINTING.md)
