"""Lint project contracts against engineering/contracts.md (Python stdlib only).

Usage: python3 contract_lint.py <contract.md>...
Prints size, lines and longest line per file, then one finding per line.
Exits 1 when any error is found; headroom warnings do not fail.
"""
import pathlib
import re
import sys

MAX_BYTES = 60 * 1024
MAX_LINES = 300
HEADROOM = 0.7
MAX_LINE = 400
BUDGET = re.compile(r'<!--\s*contract-budget:\s*bytes=(\d+)\s+lines=(\d+)\s*-->')
FENCE = re.compile(r'^\s*(```|~~~)')
HEADING = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
LINK_TARGET = re.compile(r'\]\([^)]*\)')
DATE = re.compile(r'(?<!\d)(?:19|20)\d\d-[01]\d-[0-3]\d(?!\d)')
DECISION_LOG = re.compile(
    r'\bowner (?:\w+ )?(?:chose|decided|approved|agreed|declined|answered)\b'
    r'|\bowner (?:answer|decision|choice) (?:on|in) #\d+'
    r'|\b(?:decided|agreed) (?:on|in|at|that)\b'
    r'|\b(?:formerly|historically)\b'
    r'|\b(?:was|were) (?:changed|replaced|renamed|introduced|dropped) (?:in|on|by|from|after)\b'
    r'|\b(?:since|until|as of) v?\d+\.\d+(?:\.\d+)?\b'
    r'|\bdecision log\b', re.I)
HISTORY_HEADING = re.compile(r'\b(?:history|changelog|change log|decision log|decisions|revisions?|release notes)\b', re.I)
GENERIC_HEADING = re.compile(r'^(?:misc(?:ellaneous)?|other|notes?|details?|more|general|todo|tbd)$', re.I)
PRINCIPLES = re.compile(r'^(?:\d+\.\s*)?(?:principles|rules)\b', re.I)


def lint(text):
    """Return (stats, findings); a finding is (level, line number, message)."""
    found = []
    lines = text.splitlines()
    declared = BUDGET.search(text)
    max_bytes, max_lines = map(int, declared.groups()) if declared else (MAX_BYTES, MAX_LINES)
    size = len(text.encode('utf-8'))
    for what, value, cap in (('bytes', size, max_bytes), ('lines', len(lines), max_lines)):
        if value > cap:
            found.append(('error', 0, f'{value} {what} > cap {cap}; move lowest-priority detail to a linked file'))
        elif value > cap * HEADROOM:
            found.append(('warning', 0, f'{value} {what} > {HEADROOM:.0%} of cap {cap}; no headroom left'))
    in_code = False
    longest = 0
    headings = []
    seen = {}
    prose_before_h2 = h2_seen = False
    for number, line in enumerate(lines, 1):
        if FENCE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        visible = len(LINK_TARGET.sub(']', line))
        longest = max(longest, visible)
        if visible > MAX_LINE:
            found.append(('error', number, f'line {visible} chars > {MAX_LINE}; split into one idea per paragraph'))
        for date in DATE.findall(line):
            found.append(('error', number, f'date {date}; history belongs in tasks and git'))
        for phrase in DECISION_LOG.findall(line):
            found.append(('error', number, f'decision-log phrase "{phrase}"; state the rule, not its history'))
        heading = HEADING.match(line)
        if not heading:
            if line.strip() and headings and not h2_seen and not line.lstrip().startswith('<!--'):
                prose_before_h2 = True
            continue
        level, title = len(heading.group(1)), heading.group(2)
        if not headings and level != 1:
            found.append(('error', number, 'first heading must be the H1 title'))
        if headings and level == 1:
            found.append(('error', number, 'second H1; use one title'))
        if headings and level > headings[-1][0] + 1:
            found.append(('error', number, f'heading skips from H{headings[-1][0]} to H{level}'))
        if level == 2 and not h2_seen:
            h2_seen = True
            if not prose_before_h2:
                found.append(('error', number, 'no purpose paragraph between the title and the first section'))
            if not PRINCIPLES.match(title):
                found.append(('error', number, f'first section "{title}" must be Principles or Rules'))
        if HISTORY_HEADING.search(title):
            found.append(('error', number, f'history or decision-log heading "{title}"'))
        if GENERIC_HEADING.match(title):
            found.append(('error', number, f'generic heading "{title}" does not outline content'))
        key = title.casefold()
        if key in seen:
            found.append(('error', number, f'duplicate heading "{title}" (line {seen[key]})'))
        seen.setdefault(key, number)
        headings.append((level, title))
    if not headings:
        found.append(('error', 0, 'no headings'))
    stats = {'bytes': size, 'max_bytes': max_bytes, 'lines': len(lines), 'max_lines': max_lines, 'longest': longest}
    return stats, found


def main(paths):
    if not paths:
        raise SystemExit(__doc__)
    failed = False
    for path in paths:
        stats, found = lint(pathlib.Path(path).read_text(encoding='utf-8'))
        print(f"{path}: {stats['bytes']} bytes ({stats['bytes'] / stats['max_bytes']:.0%} of {stats['max_bytes']}), "
              f"{stats['lines']} lines ({stats['lines'] / stats['max_lines']:.0%} of {stats['max_lines']}), "
              f"longest line {stats['longest']} chars (limit {MAX_LINE}), "
              f"{sum(level == 'error' for level, _, _ in found)} errors")
        for level, number, message in found:
            print(f'{path}:{number}: {level}: {message}')
        failed = failed or any(level == 'error' for level, _, _ in found)
    print('FAIL' if failed else 'PASS')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
