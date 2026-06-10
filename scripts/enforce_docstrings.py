#!/usr/bin/env python3
# enforce_docstrings.py

import sys
import os

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    errors = 0
    for i, line in enumerate(lines):
        
        if line.strip().startswith('def '):
            next_idx = i + 1
            found_docstring = False
            
            
            while next_idx < len(lines):
                next_line = lines[next_idx].strip()
                if next_line:  #
                    if next_line.startswith('"""') or next_line.startswith("'''"):
                        found_docstring = True
                    break
                next_idx += 1
            
            if not found_docstring:
                print(f"❌ Missing docstring in {filepath} at line {i+1}")
                errors += 1
    return errors

def main():
    total_errors = 0
    for root, _, files in os.walk('.'):
        # Exclude hidden and environment directories
        if '.venv' in root or '.git' in root:
            continue
        for file in files:
            if file.endswith('.py') and file != 'enforce_docstrings.py':
                total_errors += check_file(os.path.join(root, file))

    if total_errors > 0:
        print(f"\nTotal Docstring Violations: {total_errors}")
        sys.exit(1)
        
    print("Success: All functions contain a valid docstring.")
    sys.exit(0)

if __name__ == '__main__':
    main()
