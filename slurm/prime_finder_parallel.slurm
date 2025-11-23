#!/bin/bash
#SBATCH --job-name=prime_finder_parallel
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:10:00
#SBATCH --mem=4G
#SBATCH --output=prime_parallel_%j.log
#SBATCH --error=prime_parallel_%j.err

# Prime Finder Parallel - SLURM Job Script
# Uses multiprocessing to utilize multiple CPU cores
#
# The job will automatically use all available CPUs (--cpus-per-task)

# Load Python environment
module load python/3.10

# Set working directory to $SCRATCH for checkpoint persistence
cd "$SCRATCH"

# Create job-specific subdirectory
mkdir -p "prime_finder_parallel_$SLURM_JOB_ID"
cd "prime_finder_parallel_$SLURM_JOB_ID"

# Print job info
echo "Job ID: $SLURM_JOB_ID"
echo "CPUs available: $SLURM_CPUS_PER_TASK"
echo "Working directory: $(pwd)"
echo "================="

# Run parallel prime finder benchmark
# Automatically uses all available CPUs
python -m benchmarks.benchmark_parallel
