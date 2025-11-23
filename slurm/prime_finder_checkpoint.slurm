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

# Set working directory
cd "$SLURM_SUBMIT_DIR"

# Create checkpoint directory on persistent storage
export CHECKPOINT_DIR="$HOME/prime_checkpoints"
mkdir -p "$CHECKPOINT_DIR"
cd "$CHECKPOINT_DIR"

# Print job info
echo "Job ID: $SLURM_JOB_ID"
echo "Submit directory: $SLURM_SUBMIT_DIR"
echo "Checkpoint directory: $CHECKPOINT_DIR"
echo "Time limit: $SLURM_TIME_MIN minutes"
echo "=================="

# Time limit is 5 minutes SLURM time minus 30s safety buffer (270s)
# This ensures checkpoint saves before SLURM kills the job
python "$SLURM_SUBMIT_DIR"/src/prime_finder_checkpoint.py 1000000 270

# Job will checkpoint at 4.5 minutes and SLURM will requeue it
# On next submission, it resumes from saved checkpoint
