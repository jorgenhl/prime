# Parallel Prime Finder

This document describes the multiprocessing parallel implementation of the prime finder.

## Overview

The parallel version uses Python's `multiprocessing` module to distribute primality checks across
multiple CPU cores on a single machine. This provides significant speedup for CPU-intensive
operations.

## Performance

### Speedup from Parallelization

Benchmark results (5-minute runs):

| Processes | Primes Found | Rate | Speedup |
|-----------|--------------|------|---------|
| 1 (serial) | 206,000 | 679/sec | 1.0x |
| 2 | ~360,000 | 1,200/sec | 1.77x |
| 4 | ~600,000 | 2,000/sec | 2.94x |
| 8 | ~1,000,000 | 3,300/sec | 4.86x |

**Notes:**

- Speedup depends on hardware and prime size
- Not linear due to Python overhead and scheduling
- Typical speedup: `number_of_cores * 0.6-0.8`
- Larger prime numbers = better parallelization efficiency

## Usage

### Serial (Original)

```bash
python -m src.prime_finder -n 100000
```

### Parallel (Auto CPU Detection)

```bash
python -m src.prime_finder_parallel -n 100000
# Automatically uses all available CPU cores
```

### Parallel (Specific Core Count)

```bash
python -m src.prime_finder_parallel -n 100000 --processes 4
```

### Find Primes Up To Limit

```bash
python -m src.prime_finder_parallel -u 1000000
```

### Parallel Benchmark (5 minutes)

```bash
python -m benchmarks.benchmark_parallel
# Uses all CPUs automatically
```

## SLURM Integration

### Basic Parallel Job

```bash
sbatch slurm/prime_finder_parallel.slurm
```

**Configuration:**

- 4 CPUs (change `--cpus-per-task` for different core counts)
- 10 minute time limit
- Automatic checkpoint every 1,000 primes
- Automatically uses all assigned CPUs

### Parallel Job with Auto-Requeue

```bash
sbatch slurm/prime_finder_parallel_checkpoint.slurm
```

**Configuration:**

- 4 CPUs (configurable)
- 5 minute time limit per job
- Auto-requeue on timeout
- Resumes from checkpoint across job submissions

### Customize Core Count

Edit the SLURM script:

```bash
#SBATCH --cpus-per-task=8  # Use 8 cores instead of 4
```

The benchmark automatically detects and uses all available cores.

## How It Works

### Algorithm

1. **Estimate upper bound** - Uses prime number theorem to estimate where Nth prime is
1. **Divide work** - Splits range into chunks for worker processes
1. **Parallel checking** - Multiple processes check primality simultaneously
1. **Gather results** - Collect results and sort primes
1. **Expand if needed** - If not enough primes found, expand search range

### Multiprocessing Mechanics

```python
from multiprocessing import Pool

# Create pool with N worker processes
with Pool(processes=4) as pool:
    # Distribute work across workers
    results = pool.map(is_prime_with_num, numbers)
```

**How it avoids Python's GIL:**

- Each process has its own Python interpreter
- Each interpreter has its own GIL
- True parallel execution on multiple cores

## Benchmarking

### Compare Serial vs Parallel

```bash
# Run serial benchmark
time python -m benchmarks.benchmark

# Run parallel benchmark
time python -m benchmarks.benchmark_parallel

# Compare output times
```

### Parallel Benchmark with Checkpointing

```bash
# First run
python -m benchmarks.benchmark_parallel

# Interrupt (Ctrl+C) after 30 seconds
# Resume
python -m benchmarks.benchmark_parallel
# Continues from saved checkpoint
```

## Advanced Configuration

### Memory vs Speed Tradeoff

**Fewer processes = Less memory, slower**

```bash
python -m src.prime_finder_parallel -n 100000 --processes 2
```

**More processes = More memory, faster**

```bash
python -m src.prime_finder_parallel -n 100000 --processes 8
```

**Recommendation:** Use `cpu_count()` (default) for best balance

### Batch Size Optimization

Current implementation uses 1,000-prime batches. For different workloads:

- Large batches (10,000+): Better parallelization, more memory
- Small batches (100): Lower memory, more overhead

## Limitations

### What Doesn't Scale

- **Very small prime counts** (\<1,000): Overhead makes parallel slower than serial
- **Single machine only**: No cross-node distribution (use MPI for that)
- **Memory**: Large prime lists require more RAM (200k primes ~2-3 MB)

### When to Use Serial vs Parallel

**Use serial (`prime_finder.py`):**

- Finding < 10,000 primes
- Checking single numbers
- Low-memory environments

**Use parallel (`prime_finder_parallel.py`):**

- Finding > 50,000 primes
- Running on multi-core machines
- SLURM jobs with multiple CPUs
- Benchmark/performance testing

## Future Enhancements

### MPI Version (Multi-Node)

Current multiprocessing is limited to single machine. Future MPI version would:

- Distribute across multiple nodes
- Scales to 100s of cores
- Needed for very large computations

### Optimization Opportunities

- **Sieve of Eratosthenes**: Faster for finding all primes up to N
- **Segmented sieve**: Better memory efficiency
- **Caching**: Store found primes to avoid recomputation
- **Dynamic load balancing**: Adapt batch sizes based on prime density

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Parallel slower than serial | Too many small primes | Use serial for < 10k primes |
| Memory error | Too many processes | Reduce `--processes` N |
| All cores not used | Jobs competing | Use isolated SLURM allocation |
| Uneven speedup | Imbalanced load | Adjust batch size |
| Process pool hangs | Bug in worker | Check for infinite loops |

## References

- [Python multiprocessing docs](https://docs.python.org/3/library/multiprocessing.html)
- [SLURM CPU allocation](../slurm/README.md)
- [Benchmark documentation](../benchmarks/README.md)
- [Serial prime finder](../docs/README.md)
