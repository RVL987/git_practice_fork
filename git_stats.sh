#!/usr/bin/env bash

echo "(1)total number of commits:$(git -C alu_project rev-list --count HEAD)"
echo "(2)number of commits per author:$(git -C alu_project log --format="%an"|sort|uniq -c|sort -rn)"
echo "(3)the 3 most recently modified files:$(git -C alu_project log --name-only --format="" | grep -v '^$' | awk '!seen[$0]++' | head -3)"
echo "(4)the file that has been changed in the most commits:$(git -C alu_project log --diff-filter=M --name-only --format=""|sort|uniq -c|sort -rn|head -1)"
