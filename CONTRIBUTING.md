# Contributing to Prime Finder

Thank you for your interest in contributing to this HPC exploration project! This document
provides guidelines for contributing code, documentation, and feedback.

## Project Overview

This repository explores High-Performance Computing (HPC) concepts using a prime number
finder as the vehicle. The primary focus is on:

- SLURM cluster integration
- Checkpointing and fault tolerance
- Multiprocessing parallelization
- Algorithm optimization
- Documentation and testing practices

## Getting Started

### Prerequisites

- Python 3.10+
- pip (Python package manager)
- git
- Access to an 8+ core system (for benchmarking)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/jorgenhl/prime.git
cd prime

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (if any added)
pip install -r requirements.txt  # When created
```

### Run Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src

# Run linting
python -m pylint src/ benchmarks/
python -m flake8 src/ benchmarks/
python -m mdformat docs/ --check
```

## Code Standards

### Python Code Style

- **Style Guide**: PEP 8
- **Linting**: pylint (10.0/10 required), flake8 (clean)
- **Complexity**: Cyclomatic complexity < 10 per function
- **Docstrings**: Google style with Args, Returns, Raises
- **Type hints**: Not required but appreciated

Example:

```python
def find_primes_up_to(limit):
    """Find all prime numbers up to a given limit.

    Args:
        limit: Upper bound (inclusive)

    Returns:
        List of primes up to limit

    Raises:
        ValueError: If limit < 2
    """
    if limit < 2:
        raise ValueError("Limit must be >= 2")

    return [n for n in range(2, limit + 1) if is_prime(n)]
```

### Documentation Style

- **Format**: Markdown
- **Linting**: mdformat (clean, no warnings)
- **Structure**: Clear headers, code examples, links
- **Location**: `/docs/` folder

### Testing Requirements

- All new functions should have corresponding tests
- Minimum coverage: 80% for core functions
- Tests should be in `tests/` folder
- Use pytest framework

Example test:

```python
import pytest
from src.prime_finder import is_prime

class TestIsPrime:
    def test_is_prime_true(self):
        assert is_prime(17) is True
        assert is_prime(2) is True

    def test_is_prime_false(self):
        assert is_prime(1) is False
        assert is_prime(4) is False

    def test_is_prime_edge_cases(self):
        with pytest.raises(ValueError):
            is_prime(-5)
```

## Making Changes

### 1. Create a Branch

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Or bugfix branch
git checkout -b bugfix/issue-description
```

### 2. Make Your Changes

Keep changes focused and atomic:

- One feature per commit
- Clear, descriptive commit messages
- Include tests for new functionality
- Update documentation if needed

### 3. Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `ci`

Example:

```
feat: Add checkpointing to benchmark runner

- Save progress every 1000 primes
- Resume from checkpoint on restart
- Clean up checkpoint on success

Fixes #42
```

### 4. Run Quality Checks

Before pushing, ensure all checks pass:

```bash
# Run tests
python -m pytest tests/ -v

# Run linting
python -m pylint src/ benchmarks/ docs/
python -m flake8 src/ benchmarks/
python -m mdformat docs/ --check

# Check for complexity
python -m pylint --disable=all --enable=C901 src/
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:

- Clear title
- Description of changes
- Reference to related issues
- Checklist of what was tested

## Areas for Contribution

### High Priority

- [ ] Optimize prime-finding algorithm (Sieve of Eratosthenes)
- [ ] Add MPI implementation for multi-node scaling
- [ ] Improve parallel performance on small batches
- [ ] Add GPU acceleration exploration

### Medium Priority

- [ ] Add more benchmark comparisons
- [ ] Improve documentation with diagrams
- [ ] Add performance profiling tools
- [ ] Extend SLURM job templates

### Low Priority

- [ ] Add more example use cases
- [ ] Improve error messages
- [ ] Add interactive CLI options
- [ ] Create tutorial notebooks

## Pull Request Review Process

All pull requests go through review:

1. **Automated Checks**: CI pipeline verifies:

   - All tests pass
   - Linting passes (pylint 10.0/10, flake8 clean)
   - Code coverage maintained
   - No syntax errors

1. **Code Review**: Maintainer reviews for:

   - Code quality and style
   - Algorithm correctness
   - Documentation completeness
   - HPC best practices

1. **Approval**: Once approved, changes are merged

## Issues and Bug Reports

### Reporting a Bug

Include:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, core count)
- Relevant output/error messages

### Feature Requests

Include:

- Use case and motivation
- Proposed implementation (if you have one)
- Related to HPC concepts (preferred)
- Impact on existing functionality

## Benchmarking Guidelines

When optimizing or adding features:

```bash
# Run benchmark suite
python -m benchmarks.run_all_benchmarks

# Check results
cat benchmark_results.json
```

Document:

- What was changed
- Expected impact
- Actual performance difference
- System specifications used

## Documentation

### Required Documentation

- **Code**: Docstrings in Google format
- **Functions**: Description, args, returns, raises
- **Modules**: Module-level docstring
- **Features**: Corresponding docs in `/docs/`

### Documentation Location

- `/docs/README.md` - Main guide
- `/docs/PARALLEL.md` - Parallelization
- `/docs/TESTING.md` - Testing guide
- `/docs/CHECKPOINTING.md` - Checkpointing
- `/docs/BENCHMARK_REPORT.md` - Benchmarks

## Questions?

- Check existing issues and pull requests
- Review documentation in `/docs/`
- Open an issue for discussion
- Ask in pull request comments

## Code of Conduct

- Be respectful and inclusive
- Give constructive feedback
- Help others learn
- Focus on the work, not the person

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

______________________________________________________________________

Thank you for contributing! 🚀
