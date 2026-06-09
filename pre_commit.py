#!/usr/bin/env python3
import sys
import subprocess
import os

def get_staged_sv_files():
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        files = result.stdout.strip().splitlines()
        return [f for f in files if f.endswith('.sv') and os.path.exists(f)]
    except subprocess.CalledProcessError:
        return []

def check_file(filepath):
    violations = []
    
    with open(filepath, 'r', errors='ignore') as f:
        lines = f.readlines()

    first_five_text = "".join(lines[:5])
    if "Author:" not in first_five_text or "Date:" not in first_five_text:
        violations.append("Missing or invalid module header comment (Must have 'Author:' and 'Date:' in the first 5 lines)")

    for line_num, line in enumerate(lines, start=1):
        clean_line = line.rstrip('\n')
        
        if len(clean_line) > 120:
            violations.append(f"Line {line_num} exceeds 120 characters ({len(clean_line)} chars)"
       
        words = clean_line.replace(';', ' ').replace('(', ' ').replace(')', ' ').split()
        if "reg" in words:
            violations.append(f"Line {line_num} uses deprecated keyword 'reg'")

    return violations

def main():
    staged_files = get_staged_sv_files()
    failed = False

    for filepath in staged_files:
        violations = check_file(filepath)
        if violations:
            failed = True
            print(f"\nViolations found in: {filepath}")
            for v in violations:
                print(f"  - {v}")

    if failed:
        print("\nCommit blocked! Fix the errors above or use 'git commit --no-verify' if allowed.\n")
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
