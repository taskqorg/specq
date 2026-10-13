#!/bin/sh
# Print the security baseline status of every repository in a GitHub organization.
# Usage: engineering/scripts/repo-security-check.sh <org>
# Each field is a value, "absent", or "unknown" (API refused or feature unavailable).
set -eu
org=${1:?usage: $0 <org>}
q() { out=$(gh api "$1" -q "$2" 2>/dev/null) && printf '%s' "$out" || printf unknown; }
printf 'org 2fa_required=%s\n' "$(q "orgs/$org" .two_factor_requirement_enabled)"
gh repo list "$org" --limit 100 --json name,visibility,defaultBranchRef -q '.[] | "\(.name) \(.visibility) \(.defaultBranchRef.name)"' |
while read -r name vis branch; do
  r="repos/$org/$name"
  prot=$(gh api "$r/branches/$branch/protection" -q '"force_push_blocked=\(.allow_force_pushes.enabled|not) admins=\(.enforce_admins.enabled) checks=\(.required_status_checks.contexts|length)"' 2>/dev/null) || prot="protection=absent"
  sec=$(gh api "$r" -q '"secret_scanning=\(.security_and_analysis.secret_scanning.status // "unknown") push_protection=\(.security_and_analysis.secret_scanning_push_protection.status // "unknown") security_updates=\(.security_and_analysis.dependabot_security_updates.status // "unknown")"' 2>/dev/null) || sec="scanners=unknown"
  alerts=$(gh api "$r/vulnerability-alerts" >/dev/null 2>&1 && echo enabled || echo absent)
  wf=$(q "$r/actions/permissions/workflow" .default_workflow_permissions)
  secmd=$(gh api "$r/contents/SECURITY.md" >/dev/null 2>&1 && echo present || echo absent)
  printf '%s %s: %s %s vuln_alerts=%s workflow_default=%s security_md=%s\n' "$name" "$vis" "$prot" "$sec" "$alerts" "$wf" "$secmd"
done
