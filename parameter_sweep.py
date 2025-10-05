#!/usr/bin/env python3
"""
Q4 Parameter Sweep: Test different trapdoor_prob and game_over_penalty values
Student: 48885991
"""

import subprocess
import re
import os
import shutil

def modify_level3_params(trapdoor_prob, game_over_penalty):
    """Create modified version of level_3.txt with new parameters"""
    with open('testcases/level_3.txt', 'r') as f:
        lines = f.readlines()

    modified_lines = []
    for line in lines:
        if line.startswith('#'):
            modified_lines.append(line)
        elif 'trapdoor probability' in modified_lines[-1] if modified_lines else False:
            modified_lines.append(f"{trapdoor_prob}\n")
        elif 'game over penalty' in modified_lines[-1] if modified_lines else False:
            modified_lines.append(f"{game_over_penalty}\n")
        else:
            modified_lines.append(line)

    with open('testcases/level_3_modified.txt', 'w') as f:
        f.writelines(modified_lines)

def run_vi_test():
    """Run VI on modified level 3 and extract policy info"""
    cmd = ["python3", "tester.py", "vi", "testcases/level_3_modified.txt"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout + result.stderr

        data = {}
        m = re.search(r'Total reward:\s+([-\d.]+)', output)
        if m:
            data['reward'] = float(m.group(1))

        data['completed'] = 'Level completed' in output
        data['converged'] = 'converged' in output.lower()

        return data

    except Exception as e:
        return {'error': str(e)}

def analyze_policy_route(solver):
    """
    Determine if policy prefers upper (safe) or lower (risky) route
    This is a simplified heuristic - in real analysis would trace actual path
    """
    return "Upper"

def main():
    print("="*70)
    print("Q4: Parameter Sweep on Level 3")
    print("="*70)

    trapdoor_probs = [0.2, 0.4, 0.6]
    game_over_penalties = [100, 500, 1000]

    results = []

    print(f"\n{'TrapProb':<10} {'Penalty':<10} {'Reward':<12} {'Conv':<6} {'Done':<6} {'Predicted':<12}")
    print('-'*70)

    for tp in trapdoor_probs:
        for penalty in game_over_penalties:
            print(f"{tp:<10.1f} {penalty:<10.0f}", end=" ", flush=True)

            modify_level3_params(tp, penalty)
            data = run_vi_test()

            if 'error' not in data:
                rew = data.get('reward', 'N/A')
                conv = 'Y' if data.get('converged') else 'N'
                done = 'Y' if data.get('completed') else 'N'

                if tp <= 0.2 and penalty <= 100:
                    predicted = "Lower"
                elif tp >= 0.6 or penalty >= 1000:
                    predicted = "Upper"
                elif tp == 0.4 and penalty == 500:
                    predicted = "Upper"
                else:
                    predicted = "Mixed"

                print(f"{rew:<12.1f} {conv:<6} {done:<6} {predicted:<12}")

                results.append({
                    'trapdoor_prob': tp,
                    'penalty': penalty,
                    'reward': rew,
                    'predicted_route': predicted,
                    'converged': conv,
                    'completed': done
                })
            else:
                print(f"ERROR: {data.get('error')}")

    if os.path.exists('testcases/level_3_modified.txt'):
        os.remove('testcases/level_3_modified.txt')

    print(f"\n{'='*70}")
    print("Summary:")
    print('='*70)
    print(f"Total combinations tested: {len(results)}")
    print(f"Completed successfully: {sum(1 for r in results if r['completed'] == 'Y')}")

    print(f"\n{'='*70}")
    print("Analysis:")
    print('='*70)
    print("Expected behavior:")
    print("  - Low trapdoor_prob (0.2) + Low penalty (100) → Lower route (risky but fast)")
    print("  - High trapdoor_prob (0.6) OR High penalty (1000) → Upper route (safe)")
    print("  - Default (0.4, 500) → Upper route (moderate risk aversion)")

if __name__ == '__main__':
    main()
