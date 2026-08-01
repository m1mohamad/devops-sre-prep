#!/usr/bin/env python3
"""Reject duplicated interview answers, filler markers, and repeated long prose."""
from pathlib import Path
import re,sys,collections,hashlib
ROOT=Path(__file__).resolve().parents[1]; errors=[]
files=list(ROOT.glob('docs/**/*.md'))
banned=[r'\bTODO\b',r'\bTBD\b',r'lorem ipsum',r'How would you design, operate, and debug a production .* capability',r'This section intentionally left']
for p in files:
 t=p.read_text(encoding='utf-8')
 for phrase in banned:
  if re.search(phrase,t,re.I): errors.append(f'{p.relative_to(ROOT)}: placeholder/filler matches {phrase!r}')
# Exact normalized answers within each interview answer level are never useful.
t=(ROOT/'docs/interview/index.md').read_text(encoding='utf-8')
for heading in ('30-Second Answer','Strong Senior Answer','Staff-Level Expansion'):
 vals=re.findall(rf'## {re.escape(heading)}\n\n(.*?)(?=\n## |\n# |\Z)',t,re.S)
 seen={}
 for i,v in enumerate(vals,1):
  norm=re.sub(r'\W+',' ',v.lower()).strip()
  if norm in seen: errors.append(f'docs/interview/index.md: duplicate {heading} in questions {seen[norm]} and {i}')
  seen[norm]=i
if errors: print('\n'.join(errors)); sys.exit(1)
print('No duplicate interview answers or placeholder phrases found.')
