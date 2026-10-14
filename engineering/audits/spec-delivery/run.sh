#!/bin/bash
# run.sh <task> <mode> <runtime>; output in $RUNS/<task>-<mode>-<runtime>
set -u
H=$(cd "$(dirname "$0")" && pwd); O="${RUNS:?set RUNS to an empty temp dir}/$1-$2-$3"
rm -rf "$O"; mkdir -p "$O"
python3 "$H/build.py" "$1" "$2" "$3" "$O" > "$O/brief.len" || exit 1
cd "$O/repo"
start=$(date +%s)
if [ "$3" = claude ]; then
  claude -p --output-format stream-json --verbose --permission-mode dontAsk \
    --allowedTools "Bash Edit Write Read Glob Grep Skill" < "$O/brief.txt" > "$O/out.jsonl" 2> "$O/err.txt"
else
  codex exec --json -s danger-full-access --skip-git-repo-check -C "$O/repo" - < "$O/brief.txt" > "$O/out.jsonl" 2> "$O/err.txt"
fi
echo "$?" > "$O/exit"; echo $(( $(date +%s) - start )) > "$O/secs"
git -C "$O/repo" log --format='%H %s' > "$O/gitlog"; git -C "$O/repo" diff HEAD~1 --stat > "$O/diffstat" 2>/dev/null
