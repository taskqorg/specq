"""Validate local Markdown links and unmodified upstream snapshots."""
import hashlib
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
errors = []
# Tracked and untracked-unignored files; skips nested worktrees and .git.
listed = subprocess.run(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard', '*.md'],
                        cwd=ROOT, capture_output=True, text=True, check=True).stdout.split('\0')
files = [ROOT / name for name in dict.fromkeys(listed) if name and 'vendor' not in pathlib.PurePath(name).parts]
for path in files:
    text = path.read_text()
    if not text.endswith('\n'):
        errors.append(f'{path.relative_to(ROOT)}: missing final newline')
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if '://' in link or link.startswith('#'):
            continue
        target = (path.parent / link.split('#')[0]).resolve()
        if not target.is_relative_to(ROOT) or not target.exists():
            errors.append(f'{path.relative_to(ROOT)}: broken local link {link}')
manifest = json.loads((ROOT / 'caveman/vendor/caveman/source.json').read_text())
for name, entry in manifest['files'].items():
    digest = hashlib.sha256((ROOT / 'caveman/vendor/caveman' / name).read_bytes()).hexdigest()
    if digest != entry['sha256']:
        errors.append(f'Changed upstream snapshot: {name}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(files)} Markdown files; local links and upstream checksums verified.')
