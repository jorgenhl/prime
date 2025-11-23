#!/usr/bin/env python3
"""Run benchmarks for different core counts and generate report."""

import json
import os
import subprocess
import time


def select_command(cores):
    """Select which benchmark command to run.

    Args:
        cores: Number of CPU cores

    Returns:
        List of command arguments
    """
    if cores == 1:
        return ["python", "-m", "benchmarks.benchmark"]
    return ["python", "-m", "benchmarks.benchmark_parallel"]


def extract_metrics(output):
    """Extract benchmark metrics from output.

    Args:
        output: Combined stdout/stderr from benchmark

    Returns:
        Dict of extracted metrics
    """
    metrics = {}
    lines = output.split('\n')

    for line in lines:
        if "Total primes found:" in line:
            try:
                val = line.split(':')[1].replace(',', '').strip()
                metrics['total_primes'] = int(val)
            except (IndexError, ValueError):
                pass
        elif "Largest prime:" in line:
            try:
                val = line.split(':')[1].replace(',', '').strip()
                metrics['largest_prime'] = int(val)
            except (IndexError, ValueError):
                pass
        elif "Average rate:" in line and "primes/second" in line:
            try:
                rate_str = line.split(':')[1].strip().split()[0]
                metrics['rate'] = float(rate_str)
            except (IndexError, ValueError):
                pass
        elif "Completed in" in line and "seconds" in line:
            try:
                time_str = line.split("in")[1].split("seconds")[0].strip()
                metrics['time'] = float(time_str)
            except (IndexError, ValueError):
                pass

    return metrics


def run_benchmark(cores, timeout_seconds=310):
    """Run benchmark with specified cores.

    Args:
        cores: Number of CPU cores to use
        timeout_seconds: Maximum time to wait

    Returns:
        Dict with benchmark results
    """
    print(f"\n{'='*60}")
    print(f"Running benchmark with {cores} core(s)...")
    print('='*60)

    start = time.time()

    try:
        cmd = select_command(cores)
        env = os.environ.copy()
        env['PYTHONPATH'] = 'src'

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env=env,
            check=False
        )

        elapsed = time.time() - start
        output = result.stdout + result.stderr
        metrics = extract_metrics(output)

        return {
            'cores': cores,
            'success': bool(metrics),
            'elapsed': elapsed,
            'metrics': metrics
        }

    except subprocess.TimeoutExpired:
        return {
            'cores': cores,
            'success': False,
            'error': 'Timeout',
            'elapsed': timeout_seconds
        }
    except OSError as e:
        return {
            'cores': cores,
            'success': False,
            'error': str(e),
            'elapsed': time.time() - start
        }


def print_results(results):
    """Print individual benchmark results.

    Args:
        results: List of benchmark result dicts
    """
    for result in results:
        cores = result['cores']
        if result['success']:
            m = result['metrics']
            primes = m.get('total_primes', 0)
            largest = m.get('largest_prime', 0)
            rate = m.get('rate', 0)
            time_val = m.get('time', 0)

            print(f"\n✓ {cores} core(s) - Results:")
            print(f"  Primes found: {primes:,}")
            print(f"  Largest prime: {largest:,}")
            print(f"  Rate: {rate:.1f} primes/second")
            print(f"  Time: {time_val:.1f} seconds")
        else:
            error = result.get('error', 'Unknown')
            print(f"\n✗ {cores} core(s) - Failed: {error}")


def print_table(results):
    """Print results table.

    Args:
        results: List of benchmark result dicts
    """
    print("\n" + "="*60)
    print("BENCHMARK REPORT")
    print("="*60)

    header = f"\n{'Cores':<8} {'Primes':<15} {'Rate (p/s)':<15}"
    header += f" {'Time (s)':<12}"
    print(header)
    print("-" * 60)

    baseline_rate = None
    for result in results:
        if result['success']:
            m = result['metrics']
            cores = result['cores']
            primes = m.get('total_primes', 0)
            rate = m.get('rate', 0)
            time_s = m.get('time', 0)

            row = f"{cores:<8} {primes:<15,} {rate:<15.1f}"
            row += f" {time_s:<12.1f}"
            print(row)

            if cores == 1:
                baseline_rate = rate

    # Speedup analysis
    print("\n" + "-"*60)
    print("SPEEDUP ANALYSIS (relative to 1 core):")
    print("-" * 60)

    if baseline_rate:
        for result in results:
            if result['success']:
                m = result['metrics']
                cores = result['cores']
                rate = m.get('rate', 0)
                speedup = rate / baseline_rate

                print(f"{cores} core(s): {speedup:.2f}x")


def main():
    """Run benchmarks and generate report."""
    print("\n" + "="*60)
    print("PRIME FINDER BENCHMARK SUITE")
    print("="*60)
    print("Testing cores: 1, 2, 4, 6")
    print("Each benchmark runs for ~5 minutes")
    print("="*60)

    results = []

    for cores in [1, 2, 4, 6]:
        result = run_benchmark(cores)
        results.append(result)

    # Print results
    print_results(results)

    # Print table
    print_table(results)

    # Save to JSON
    with open('benchmark_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print("\n✓ Results saved to benchmark_results.json")


if __name__ == "__main__":
    main()
