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
# Finds the first N prime numbers

# Load Python environment
module load python/3.10

# Set working directory
cd "$SLURM_SUBMIT_DIR"

# Run prime finder
# Arguments: target_count [max_time_seconds]
python -m benchmarks.benchmark
