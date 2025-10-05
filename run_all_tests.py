#!/usr/bin/env python3
"""
Run all tests for report data collection
Student: 48885991
"""

import subprocess
import re
import json
from datetime import datetime

def run_test(algorithm, level):
    """Run a single test and parse output"""
    cmd = ["python3", "tester.py", algorithm, f"testcases/level_{level}.txt"]
    print(f"  Running {algorithm.upper()} on level {level}...", end=" ", flush=True)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout + result.stderr

        data = {
            'level': level,
            'algorithm': algorithm.upper(),
            'raw_output': output
        }

        m = re.search(r'Number of Iterations:\s+(\d+)', output)
        if m:
            data['iterations'] = int(m.group(1))

        m = re.search(r'iterations max target:\s+(\d+)', output)
        if m:
            data['iter_target'] = int(m.group(1))

        m = re.search(r'Average time taken per iteration:\s+([\d.]+)', output)
        if m:
            data['avg_time'] = float(m.group(1))

        m = re.search(r'average time max target:\s+([\d.]+)', output)
        if m:
            data['time_target'] = float(m.group(1))

        m = re.search(r'Maximum time taken per iteration:\s+([\d.]+)', output)
        if m:
            data['max_time'] = float(m.group(1))

        m = re.search(r'Total reward:\s+([-\d.]+)', output)
        if m:
            data['reward'] = float(m.group(1))

        m = re.search(r'reward max target:\s+([-\d.]+)', output)
        if m:
            data['reward_target'] = float(m.group(1))

        data['converged'] = 'converged' in output.lower()
        data['completed'] = 'Level completed' in output

        print("✓")
        return data

    except subprocess.TimeoutExpired:
        print("✗ (timeout)")
        return {'level': level, 'algorithm': algorithm.upper(), 'error': 'timeout'}
    except Exception as e:
        print(f"✗ ({str(e)})")
        return {'level': level, 'algorithm': algorithm.upper(), 'error': str(e)}

def main():
    print("="*70)
    print("COMP3702 Assignment 2 - Comprehensive Test Suite")
    print(f"Student: 48885991")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    algorithms = ['vi', 'pi', 'ql']
    levels = [1, 2, 3, 4, 5]

    all_results = []

    for level in levels:
        print(f"\n{'='*70}")
        print(f"LEVEL {level}")
        print('='*70)

        for alg in algorithms:
            data = run_test(alg, level)
            all_results.append(data)

    with open('test_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)

    print(f"\n{'='*70}")
    print("SUMMARY")
    print('='*70)
    print(f"{'Lvl':<4} {'Alg':<4} {'Iter':<8} {'Target':<8} {'AvgTime':<10} {'Target':<10} {'Reward':<10} {'Target':<10} {'Conv':<5} {'Done':<5}")
    print('-'*70)

    for r in all_results:
        if 'error' not in r:
            iters = str(r.get('iterations', '-'))
            iter_tgt = str(r.get('iter_target', '-'))
            avg_t = f"{r.get('avg_time', 0):.4f}" if 'avg_time' in r else '-'
            time_tgt = f"{r.get('time_target', 0):.4f}" if 'time_target' in r else '-'
            rew = f"{r.get('reward', 0):.1f}" if 'reward' in r else '-'
            rew_tgt = f"{r.get('reward_target', 0):.1f}" if 'reward_target' in r else '-'
            conv = 'Y' if r.get('converged') else 'N'
            done = 'Y' if r.get('completed') else 'N'

            print(f"{r['level']:<4} {r['algorithm']:<4} {iters:<8} {iter_tgt:<8} {avg_t:<10} {time_tgt:<10} {rew:<10} {rew_tgt:<10} {conv:<5} {done:<5}")
        else:
            print(f"{r['level']:<4} {r['algorithm']:<4} ERROR: {r.get('error', 'unknown')}")

    print(f"\n{'='*70}")
    print("Analysis by Algorithm:")
    print('='*70)

    for alg in algorithms:
        alg_results = [r for r in all_results if r['algorithm'] == alg.upper() and 'error' not in r]
        if alg_results:
            total_iters = sum(r.get('iterations', 0) for r in alg_results)
            avg_iters = total_iters / len(alg_results)
            completed = sum(1 for r in alg_results if r.get('completed'))
            converged = sum(1 for r in alg_results if r.get('converged'))

            print(f"\n{alg.upper()}:")
            print(f"  Completed: {completed}/{len(alg_results)} levels")
            print(f"  Converged: {converged}/{len(alg_results)} levels")
            print(f"  Avg iterations: {avg_iters:.1f}")

    print(f"\n{'='*70}")
    print("Results saved to test_results.json")
    print('='*70)

if __name__ == '__main__':
    main()
