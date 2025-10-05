#!/usr/bin/env python3
"""
Collect experimental results for report
"""

import subprocess
import re
import sys

def run_test(algorithm, level):
    """Run tester and parse output"""
    cmd = f"python3 tester.py {algorithm} testcases/level_{level}.txt"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        output = result.stdout + result.stderr

        data = {}
        data['level'] = level
        data['algorithm'] = algorithm.upper()

        m = re.search(r'Number of Iterations:\s+(\d+)', output)
        if m:
            data['iterations'] = int(m.group(1))

        m = re.search(r'Average time taken per iteration:\s+([\d.]+)', output)
        if m:
            data['avg_time'] = float(m.group(1))

        m = re.search(r'Maximum time taken per iteration:\s+([\d.]+)', output)
        if m:
            data['max_time'] = float(m.group(1))

        m = re.search(r'Total reward:\s+([-\d.]+)', output)
        if m:
            data['reward'] = float(m.group(1))

        data['converged'] = 'converged' in output.lower()
        data['completed'] = 'Level completed' in output

        return data
    except subprocess.TimeoutExpired:
        return {'level': level, 'algorithm': algorithm.upper(), 'error': 'timeout'}
    except Exception as e:
        return {'level': level, 'algorithm': algorithm.upper(), 'error': str(e)}

if __name__ == '__main__':
    algorithms = ['vi', 'pi', 'ql']
    levels = [1, 2, 3]

    results = []
    for level in levels:
        print(f"\n{'='*60}")
        print(f"Level {level}")
        print('='*60)
        for alg in algorithms:
            print(f"Running {alg.upper()}...")
            data = run_test(alg, level)
            results.append(data)

            if 'error' in data:
                print(f"  ERROR: {data['error']}")
            else:
                print(f"  Iterations: {data.get('iterations', 'N/A')}")
                print(f"  Avg time: {data.get('avg_time', 'N/A')}")
                print(f"  Reward: {data.get('reward', 'N/A')}")
                print(f"  Converged: {data.get('converged', False)}")
                print(f"  Completed: {data.get('completed', False)}")

    print(f"\n{'='*60}")
    print("SUMMARY TABLE")
    print('='*60)
    print(f"{'Level':<7} {'Alg':<5} {'Iters':<7} {'AvgTime':<10} {'Reward':<10} {'Conv':<6} {'Done':<6}")
    print('-'*60)
    for r in results:
        if 'error' not in r:
            print(f"{r['level']:<7} {r['algorithm']:<5} {r.get('iterations', '-'):<7} "
                  f"{r.get('avg_time', '-'):<10} {r.get('reward', '-'):<10} "
                  f"{'Y' if r.get('converged') else 'N':<6} {'Y' if r.get('completed') else 'N':<6}")
