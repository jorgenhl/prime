#!/bin/bash
#SBATCH --job-name=prime_finder_ckpt
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:05:00
#SBATCH --mem=4G
#SBATCH --requeue
#SBATCH --output=prime_ckpt_%j.log
#SBATCH --error=prime_ckpt_%j.err

# Prime Finder with Checkpointing - SLURM Job Script
# Automatically saves progress and resumes on timeout/failure
#
# Usage:
#   sbatch prime_finder_checkpoint.slurm
#
# The job will:
# 1. Run for up to 5 minutes
# 2. Save checkpoint before timeout
# 3. Auto-requeue to continue from saved state
#
# Monitor with:
#   squeue -u $USER
#   tail -f prime_ckpt_*.log

# Load Python environment
module load python/3.10

# Set working directory to $SCRATCH for checkpoint persistence
# Use consistent directory so checkpoints persist across requeues
export CHECKPOINT_DIR="$SCRATCH/prime_finder_main"
mkdir -p "$CHECKPOINT_DIR"
cd "$CHECKPOINT_DIR"

# Print job info
echo "Job ID: $SLURM_JOB_ID"
echo "Working directory: $CHECKPOINT_DIR"
echo "Time limit: $SLURM_TIME_MIN minutes"
echo "=================="

# Run prime finder with checkpointing
# Checkpoint automatically saves/loads from current directory
python -m benchmarks.benchmark

# Job will checkpoint after 5 minutes and SLURM will requeue it
# On next submission, it resumes from saved checkpoint
