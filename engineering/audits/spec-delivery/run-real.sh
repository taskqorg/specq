#!/bin/bash
# run-real.sh <task> <mode> <runtime>; output in $RUNS/<task>-<mode>-<runtime>; 45 min cap per run
# Permissions replay the taskq worker defaults (taskq.md R9) on fixed public task texts in throwaway clones; run only on a host where that is acceptable.
set -u
H=$(cd "$(dirname "$0")" && pwd); O="${RUNS:?set RUNS to an empty temp dir}/$1-$2-$3"
rm -rf "$O"; mkdir -p "$O"
python3 "$H/real.py" "$1" "$2" "$3" "$O" > "$O/brief.len" || exit 1
cd "$O/repo"
start=$(date +%s)
if [ "$3" = claude ]; then
  set -- perl -e 'alarm 2700; exec @ARGV' claude -p --output-format stream-json --verbose --permission-mode dontAsk \
    --allowedTools "Bash Edit Write Read Glob Grep Skill"
else
  set -- perl -e 'alarm 2700; exec @ARGV' codex exec --json -s danger-full-access --skip-git-repo-check -C "$O/repo" -
fi
"$@" < "$O/brief.txt" > "$O/out.jsonl" 2> "$O/err.txt"
echo "$?" > "$O/exit"; echo $(( $(date +%s) - start )) > "$O/secs"
git -C "$O/repo" log --format='%H %s' origin/HEAD..HEAD > "$O/gitlog" 2>/dev/null || git -C "$O/repo" log -3 --format='%H %s' > "$O/gitlog"
