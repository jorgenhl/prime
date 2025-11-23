#!/usr/bin/env python3
"""Run benchmarks for different core counts and generate report."""

import subprocess
import time
import json

def run_benchmark(cores, timeout_seconds=310):
    """Run benchmark with specified cores."""
    print(f"\n{'='*60}")
    print(f"Running benchmark with {cores} core(s)...")
    print('='*60)
    
    start = time.time()
    
    try:
        if cores == 1:
            # Serial benchmark (5 minutes using time-based benchmark)
            cmd = ["python", "-m", "benchmarks.benchmark"]
        else:
            # Parallel benchmark (find specific number of primes)
            cmd = ["python", "-m", "benchmarks.benchmark_parallel"]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env={**subprocess.os.environ, 'PYTHONPATH': 'src'}
        )
        
        elapsed = time.time() - start
        output = result.stdout + result.stderr
        
        # Extract key metrics
        lines = output.split('\n')
        metrics = {}
        
        for line in lines:
            if "Total primes found:" in line:
                try:
                    metrics['total_primes'] = int(
                        line.split(':')[1].replace(',', '').strip())
                except (IndexError, ValueError):
                    pass
            elif "Largest prime:" in line:
                try:
                    metrics['largest_prime'] = int(
                        line.split(':')[1].replace(',', '').strip())
                except (IndexError, ValueError):
                    pass
            elif "Average rate:" in line or "Processes used" not in line and "primes/second" in line:
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
    except Exception as e:
        return {
            'cores': cores,
            'success': False,
            'error': str(e),
            'elapsed': time.time() - start
        }

def main():
    """Run benchmarks and generate report."""
    print("\n" + "="*60)
    print("PRIME FINDER BENCHMARK SUITE")
    print("="*60)
    print(f"Testing cores: 1, 2, 4, 6")
    print(f"Each benchmark runs for ~5 minutes")
    print("="*60)
    
    results = []
    
    for cores in [1, 2, 4, 6]:
        result = run_benchmark(cores)
        results.append(result)
        
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
            print(f"\n✗ {cores} core(s) - Failed: {result.get('error', 'Unknown')}")
    
    # Generate report
    print("\n" + "="*60)
    print("BENCHMARK REPORT")
    print("="*60)
    
    # Table format
    print(f"\n{'Cores':<8} {'Primes':<15} {'Rate (p/s)':<15} {'Time (s)':<12}")
    print("-" * 60)
    
    baseline_rate = None
    for result in results:
        if result['success']:
            m = result['metrics']
            cores = result['cores']
            primes = m.get('total_primes', 0)
            rate = m.get('rate', 0)
            time_s = m.get('time', 0)
            
            print(f"{cores:<8} {primes:<15,} {rate:<15.1f} {time_s:<12.1f}")
            
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
                speedup = rate / baseline_rate if baseline_rate else 0
                
                print(f"{cores} core(s): {speedup:.2f}x")
    
    # Save to JSON
    with open('benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n✓ Results saved to benchmark_results.json")

if __name__ == "__main__":
    main()
