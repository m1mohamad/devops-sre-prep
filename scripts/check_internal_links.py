#!/usr/bin/env python3
"""Validate relative Markdown links without requiring MkDocs-specific syntax."""
from pathlib import Path
from urllib.parse import unquote
import re,sys
ROOT=Path(__file__).resolve().parents[1]; errors=[]
for path in ROOT.glob('docs/**/*.md'):
 text=path.read_text(encoding='utf-8')
 for target in re.findall(r'(?<!!)\[[^]]+\]\(([^)]+)\)',text):
  target=target.split()[0].strip('<>').split('#',1)[0]
  if not target or re.match(r'^(https?://|mailto:)',target): continue
  dest=(path.parent/unquote(target)).resolve()
  if dest.is_dir(): dest=dest/'index.md'
  if dest.suffix=='': dest=dest.with_suffix('.md')
  if ROOT not in dest.parents and dest != ROOT: errors.append(f'{path.relative_to(ROOT)}: link escapes repository: {target}')
  elif not dest.exists(): errors.append(f'{path.relative_to(ROOT)}: broken link: {target}')
if errors: print('\n'.join(errors)); sys.exit(1)
print('Internal Markdown links valid.')
