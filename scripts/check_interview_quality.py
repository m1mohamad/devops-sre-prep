#!/usr/bin/env python3
"""Validate exact-question structure and cross-question uniqueness."""
from pathlib import Path
from collections import defaultdict
import re,sys
ROOT=Path(__file__).resolve().parents[1]; req=['30-Second Answer','Strong Senior Answer','Staff-Level Expansion','Diagram or Decision Flow','Commands or Evidence','Likely Follow-ups','Common Weak Answer','Experience Prompt']; seen={h:defaultdict(list) for h in req}; errors=[]; count=0
for p in (ROOT/'docs/interview').glob('*.md'):
 if p.name=='index.md': continue
 chunks=re.split(r'(?m)(?=^## Question\n)',p.read_text())[1:]
 for n,c in enumerate(chunks,1):
  count+=1
  for h in req:
   m=re.search(rf'^## {re.escape(h)}\n\n(.*?)(?=\n## |\Z)',c,re.M|re.S)
   if not m: errors.append(f'{p.name} question {n}: missing {h}'); continue
   v=re.sub(r'\W+',' ',m.group(1).lower()).strip(); seen[h][v].append(f'{p.name}:{n}')
for h,d in seen.items():
 for v,where in d.items():
  if len(where)>2: errors.append(f'identical {h} in {where}')
for phrase in ['walk the concrete handoffs','define the failure domain and the team that owns','stronger isolation reduces correlated failure','give a real example with this mechanism']:
 occurrences=sum(p.read_text().lower().count(phrase) for p in (ROOT/'docs/interview').glob('*.md'))
 if occurrences>2: errors.append(f'generic phrase repeated {occurrences} times: {phrase}')
if not 45<=count<=60: errors.append(f'expected 45-60 questions, found {count}')
if errors: print('\n'.join(errors));sys.exit(1)
print(f'Interview quality valid ({count} questions checked).')
