# Prime Finder

> **Note:** This repository is an exploration of High-Performance Computing (HPC) features
> including SLURM integration, checkpointing, multiprocessing parallelization, and cluster
> job management. While the prime finder is a fully functional tool, the primary purpose is
> to demonstrate HPC patterns and best practices for computational research.

A Python tool to find and check prime numbers with multiple modes and SLURM checkpointing
support for HPC clusters.

## Quick Start

```bash
# Check if a number is prime
python -m src.prime_finder 17

# Find all primes up to a limit
python -m src.prime_finder -u 30

# Find the first N primes
python -m src.prime_finder -n 10

# Run 5-minute performance benchmark
python -m benchmarks.benchmark

# Submit to HPC cluster (SLURM)
sbatch slurm/prime_finder.slurm
sbatch slurm/prime_finder_checkpoint.slurm
```

## Features

### Core Functionality

- **Single number check**: Verify whether a single number is prime
- **Range search**: Generate all prime numbers up to a specified value
- **First N primes**: Generate the first N prime numbers
- **Both serial and parallel**: Single-threaded and multiprocessing implementations

### Performance & Benchmarking

- **5-minute benchmarks**: Automated performance testing suite
- **Multi-core benchmarking**: Compare performance across 1, 2, 4, and 6 cores
- **Detailed reporting**: JSON output with metrics and speedup analysis
- **Checkpointing**: Resume benchmarks from saved progress

### HPC & Cluster Features

- **SLURM integration**: Job submission scripts for batch processing
- **Checkpointing**: Resume from interruptions on SLURM clusters
- **Auto-requeue**: Automatic job resubmission on timeout
- **$SCRATCH support**: Cluster-accessible checkpoint storage
- **Multiprocessing**: Parallel execution using Python's multiprocessing module

### Quality Assurance

- **Comprehensive tests**: Unit and integration test suite
- **High code quality**: pylint 10.0/10, flake8 clean, mdformat verified
- **Low cyclomatic complexity**: Functions designed for maintainability
- **Full documentation**: Usage guides, API docs, and examples

## Requirements

- Python 3.10+
- pip (for dependency installation)
- pytest, pylint, flake8, mdformat (for development)

See `requirements.txt` for full dependency list.

## Documentation

Complete documentation is organized in the `/docs/` folder:

- **[README](docs/README.md)** - Full usage guide and algorithm explanation
- **[PARALLEL](docs/PARALLEL.md)** - Multiprocessing parallelization guide and performance analysis
- **[TESTING](docs/TESTING.md)** - Test suite documentation and performance metrics
- **[CHECKPOINTING](docs/CHECKPOINTING.md)** - HPC cluster checkpointing implementation guide
- **[BENCHMARK_REPORT](docs/BENCHMARK_REPORT.md)** - Detailed benchmark results and analysis

Additional resources:

- **[CONTRIBUTING](CONTRIBUTING.md)** - Contribution guidelines and code standards
- **[LICENSE](LICENSE)** - MIT License
- **[SLURM Scripts](slurm/README.md)** - Job submission scripts and cluster integration

## Quick Performance Reference

Found **206,000 primes in 5 minutes** with largest prime **2,838,169**.

Average throughput: **679 primes/second**

See [Performance Metrics](docs/TESTING.md#performance-metrics) for details.

## Development

### Run Tests

```bash
python -m pytest tests/test_prime_finder.py -v
```

### Run Linting

```bash
# Python linting
python -m pylint src/ benchmarks/ tests/
python -m flake8 src/ benchmarks/ tests/

# Markdown linting
python -m mdformat docs/ README.md CONTRIBUTING.md --check
```

### Running Benchmark

```bash
python -m benchmarks.benchmark
```

## Project Structure

```
.
├── src/
│   ├── __init__.py                      # Package marker
│   ├── prime_finder.py                  # Serial implementation
│   └── prime_finder_parallel.py         # Parallel (multiprocessing) implementation
├── tests/
│   └── test_prime_finder.py             # Unit tests
├── benchmarks/
│   ├── benchmark.py                     # 5-minute serial benchmark
│   ├── benchmark_parallel.py            # 5-minute parallel benchmark
│   └── run_all_benchmarks.py            # Multi-core benchmark suite
├── slurm/
│   ├── prime_finder.slurm               # Basic job script
│   ├── prime_finder_checkpoint.slurm    # Auto-requeue job script
│   ├── prime_finder_parallel.slurm      # Parallel job script
│   ├── prime_finder_parallel_checkpoint.slurm  # Parallel auto-requeue
│   └── README.md                        # SLURM documentation
├── docs/
│   ├── README.md                        # Full usage guide
│   ├── PARALLEL.md                      # Parallelization guide
│   ├── TESTING.md                       # Testing documentation
│   ├── CHECKPOINTING.md                 # HPC checkpointing guide
│   └── BENCHMARK_REPORT.md              # Benchmark analysis
├── .github/
│   └── workflows/
│       └── python-app.yml               # CI/CD pipeline
├── CONTRIBUTING.md                      # Contribution guidelines
├── LICENSE                              # MIT License
├── requirements.txt                     # Python dependencies
└── README.md                            # This file
```

## Algorithm

Trial division with √n optimization for efficient prime checking. See
[Algorithm](docs/README.md#algorithm) for detailed explanation.

## License

MIT
