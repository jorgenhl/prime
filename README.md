# Prime Finder

A Python tool to find and check prime numbers with multiple modes and SLURM checkpointing
support for HPC clusters.

## Quick Start

```bash
# Check if a number is prime
python prime_finder.py 17

# Find all primes up to a limit
python prime_finder.py -u 30

# Find the first N primes
python prime_finder.py -n 10

# Run 5-minute performance benchmark
python benchmark.py
```

## Features

- **Check if prime**: Verify whether a single number is prime
- **Find primes up to limit**: Generate all prime numbers up to a specified value
- **Find first N primes**: Generate the first N prime numbers
- **Benchmarking**: 5-minute performance tests
- **HPC checkpointing**: Resume from interruptions on SLURM clusters

## Requirements

- Python 3.6+

## Documentation

- **[README](docs/README.md)** - Full usage guide and algorithm explanation
- **[TESTING](docs/TESTING.md)** - Test suite documentation and performance metrics
- **[CHECKPOINTING](docs/CHECKPOINTING.md)** - HPC cluster checkpointing implementation guide

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
python -m pylint src/prime_finder.py tests/test_prime_finder.py benchmarks/benchmark.py
python -m flake8 src/prime_finder.py tests/test_prime_finder.py benchmarks/benchmark.py
python -m mdformat --check docs/*.md README.md
```

### Running Benchmark

```bash
python -m benchmarks.benchmark
```

## Project Structure

```
.
├── src/
│   ├── __init__.py              # Package marker
│   └── prime_finder.py           # Main module
├── tests/
│   └── test_prime_finder.py      # Unit tests (24 test cases)
├── benchmarks/
│   └── benchmark.py              # 5-minute performance benchmark
├── docs/
│   ├── README.md                 # Full documentation
│   ├── TESTING.md                # Testing guide
│   └── CHECKPOINTING.md          # HPC cluster checkpointing guide
├── .github/
│   └── workflows/
│       └── python-app.yml        # CI/CD with pylint, flake8, mdformat, pytest
└── README.md                      # This file
```

## Algorithm

Trial division with √n optimization for efficient prime checking. See
[Algorithm](docs/README.md#algorithm) for detailed explanation.

## License

MIT
