# Benchmark Suite

This folder contains performance benchmarking scripts for the prime finder.

## Overview

Benchmarks measure how efficiently the prime finder can discover prime numbers under various
conditions. Results help understand algorithm performance and identify optimization opportunities.

## Scripts

### `benchmark.py`

5-minute continuous prime finding performance test.

**Purpose:** Measure sustained throughput and largest prime found in a fixed time window.

**Usage:**

```bash
python -m benchmarks.benchmark
```

**Output:**

```
Starting 5-minute prime finder benchmark...
============================================================
[  1.3s] Found   1000 primes. Largest:    7919
[ 10.5s] Found  10000 primes. Largest:  104729
[100.2s] Found 100000 primes. Largest: 1299709
[303.3s] Found 206000 primes. Largest: 2838169
============================================================

Completed in 303.3 seconds
Total primes found: 206,000
Largest prime: 2,838,169
Average rate: 679.5 primes/second
```

## Benchmark Results

### Hardware Reference

Baseline results on typical hardware (reference only):

| Metric | Value |
|--------|-------|
| Duration | 5 minutes (300 seconds) |
| Primes Found | 206,000 |
| Largest Prime | 2,838,169 |
| Average Rate | 679 primes/second |

### Performance Characteristics

- **Linear scaling**: Finding N primes takes roughly O(N×√n) time
- **Memory efficient**: Only stores final prime list (~2-3 MB for 200k primes)
- **Single-threaded**: No parallelization (good for HPC resource efficiency)

## How to Run Benchmarks

### Local Testing

```bash
# Run 5-minute benchmark
python -m benchmarks.benchmark

# Run with time limit (30 seconds)
timeout 30 python -m benchmarks.benchmark
```

### On HPC Cluster with SLURM

```bash
# Submit to cluster
sbatch ../slurm/prime_finder.slurm

# Monitor progress
watch -n 5 'tail -20 prime_*.log'
```

## Interpreting Results

### Throughput

**Average rate** = Total primes / Time elapsed

```
206,000 primes / 303.3 seconds ≈ 679 primes/second
```

Higher rates indicate better algorithm efficiency. Rates typically:

- **Decrease over time**: As primes get larger, checking takes longer
- **Scale with hardware**: Better CPUs find primes faster

### Scaling

For N primes, expected time grows as O(N × √p) where p is the Nth prime.

```
Finding 1,000 primes   ≈ 0.1 seconds
Finding 10,000 primes  ≈ 1.5 seconds
Finding 100,000 primes ≈ 150 seconds
```

### Optimization Opportunities

- **Sieve of Eratosthenes**: Faster for finding all primes up to N (vs finding Nth prime)
- **Parallel processing**: MPI/OpenMP for multi-node clusters
- **Segmented sieves**: Better memory efficiency for very large ranges
- **Caching**: Store primes to avoid recomputation

## Comparing Runs

### Track Performance Over Time

Create a log of benchmark runs:

```bash
# Run and save results
python -m benchmarks.benchmark | tee benchmark_run_$(date +%s).log

# Compare multiple runs
diff benchmark_run_1700729400.log benchmark_run_1700729700.log
```

### Expected Variance

- **Small variance** (±5%): Normal due to system load
- **Large variance** (>10%): Check for:
  - Background processes
  - CPU frequency scaling
  - Thermal throttling
  - Filesystem caching differences

## Use Cases

### Validating Algorithm Changes

Before/after benchmark comparison:

```bash
# Original version
python -m benchmarks.benchmark > before.txt

# Make code changes...

# Optimized version
python -m benchmarks.benchmark > after.txt

# Compare
diff before.txt after.txt
```

### Hardware Comparison

Compare different systems:

```bash
# On system A
python -m benchmarks.benchmark

# On system B
python -m benchmarks.benchmark

# Results show which hardware is faster
```

### Capacity Planning

Estimate resources needed for large computations:

```
To find 1,000,000 primes:
- Estimated time: ~1.5 hours (at 679 primes/second)
- Memory needed: ~15 MB
- SLURM time request: 2 hours (with buffer)
```

## Limitations

### What This Benchmark Measures

- **Single-machine performance**: Not distributed/parallel
- **Sequential efficiency**: Not I/O, networking, or concurrent workloads
- **Best-case scenario**: No external load or interruptions

### What This Benchmark Doesn't Measure

- **Parallel scaling**: Multi-process/MPI efficiency
- **Cluster overhead**: Job startup, checkpoint I/O
- **Fault tolerance**: Recovery time from failures
- **Memory pressure**: Behavior when low on RAM

## Advanced: Profiling

### CPU Profiling

```bash
# Install profiler
pip install py-spy

# Profile the benchmark
py-spy record -o profile.svg -- python -m benchmarks.benchmark

# View results
open profile.svg
```

### Memory Profiling

```bash
# Install memory profiler
pip install memory-profiler

# Profile memory usage
python -m memory_profiler benchmarks/benchmark.py
```

## References

- [sqrt(n) Optimization](../docs/README.md#algorithm) - Algorithm explanation
- [Performance Metrics](../docs/TESTING.md#performance-metrics) - Test results
- [SLURM Integration](../slurm/README.md) - Running on clusters
