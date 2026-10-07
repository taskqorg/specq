"""Validate local Markdown links and unmodified upstream snapshots."""
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
errors = []
files = [p for p in ROOT.rglob('*.md') if 'vendor' not in p.relative_to(ROOT).parts]
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
manifest = json.loads((ROOT / 'vendor/caveman/source.json').read_text())
for name, entry in manifest['files'].items():
    digest = hashlib.sha256((ROOT / 'vendor/caveman' / name).read_bytes()).hexdigest()
    if digest != entry['sha256']:
        errors.append(f'Changed upstream snapshot: {name}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(files)} Markdown files; local links and upstream checksums verified.')
