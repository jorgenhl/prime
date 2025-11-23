#!/bin/bash
#SBATCH --job-name=prime_finder
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:10:00
#SBATCH --mem=4G
#SBATCH --output=prime_%j.log
#SBATCH --error=prime_%j.err

# Prime Finder - Basic SLURM Job Script
# Finds the first N prime numbers with checkpointing

# Load Python environment
module load python/3.10

# Set working directory to $SCRATCH for checkpoint persistence
cd "$SCRATCH"

# Create job-specific subdirectory
mkdir -p "prime_finder_$SLURM_JOB_ID"
cd "prime_finder_$SLURM_JOB_ID"

# Run prime finder with checkpointing
# Checkpoint automatically saves to $SCRATCH/prime_finder_$SLURM_JOB_ID/
python -m benchmarks.benchmark

