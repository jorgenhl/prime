#!/bin/bash
#SBATCH --job-name=prime_finder_parallel_ckpt
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:05:00
#SBATCH --mem=4G
#SBATCH --requeue
#SBATCH --output=prime_parallel_ckpt_%j.log
#SBATCH --error=prime_parallel_ckpt_%j.err

# Prime Finder Parallel with Checkpointing - SLURM Job Script
# Uses multiprocessing and auto-requeuing for long-running jobs
#
# Features:
# - Multiprocessing: Uses all available CPUs (--cpus-per-task)
# - Auto-requeue: Automatically continues on timeout
# - Checkpointing: Resumes from previous progress
#
# Monitor with:
#   squeue -u $USER
#   tail -f prime_parallel_ckpt_*.log
#   cat $SCRATCH/prime_finder_parallel_main/benchmark_parallel_checkpoint.json

# Load Python environment
module load python/3.10

# Set working directory to $SCRATCH for checkpoint persistence
# Use consistent directory so checkpoints persist across requeues
export CHECKPOINT_DIR="$SCRATCH/prime_finder_parallel_main"
mkdir -p "$CHECKPOINT_DIR"
cd "$CHECKPOINT_DIR"

# Print job info
echo "Job ID: $SLURM_JOB_ID"
echo "CPUs available: $SLURM_CPUS_PER_TASK"
echo "Working directory: $CHECKPOINT_DIR"
echo "Time limit: $SLURM_TIME_MIN minutes"
echo "================="

# Run parallel prime finder benchmark with checkpointing
# Automatically uses all available CPUs and resumes from checkpoint
python -m benchmarks.benchmark_parallel

# Job will checkpoint after 5 minutes and SLURM will requeue it
# On next submission, it resumes from saved checkpoint using same CPUs
