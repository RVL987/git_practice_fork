#!/usr/bin/env python3
import sys, os, subprocess
from datetime import datetime

if len(sys.argv) < 2:
    print("Usage: python3 analyze_repo.py <local_path_or_git_url>")
    sys.exit(1)

target = sys.argv[1]
if target.startswith("http"):
    repo_name = target.split("/")[-1].replace(".git", "")
    subprocess.run(["git", "clone", target, repo_name])
    os.chdir(repo_name)
else:
    os.chdir(target)

log_data = subprocess.check_output(["git", "log", "--format=%aI|%an"], text=True).strip().split("\n")
commits = []
contributors = {}

for line in log_data:
    iso_date, author = line.split("|", 1)
    dt = datetime.fromisoformat(iso_date.split("+")[0].split("-")[0] if iso_date.count("-")==3 else iso_date.split("+")[0])
    commits.append(dt)
    contributors[author] = contributors.get(author, 0) + 1

commits.sort()
total_commits = len(commits)

months = [c.strftime("%Y-%m") for c in commits if (datetime.now() - c).days <= 365]
month_counts = {m: months.count(m) for m in set(months)}
top_5 = sorted(contributors.items(), key=lambda x: x[1], reverse=True)[:5]
total_days = (commits[-1] - commits[0]).days + 1
gaps = [commits[i] - commits[i-1] for i in range(1, len(commits))]
longest_gap = max(gaps) if gaps else bytes(0)

print(f"Total Commits: {total_commits}")
print(f"Avg Commits/Day: {total_commits / total_days:.2f}")
print(f"Longest Gap: {longest_gap.days} days")
print("\nTop Contributors:", top_5)
print("\nCommits Per Month (Last 12 Months):", sorted(month_counts.items(), reverse=True))
