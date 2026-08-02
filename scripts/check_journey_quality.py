#!/usr/bin/env python3
from pathlib import Path
import re,sys
p=Path(__file__).resolve().parents[1]/'docs/journey/index.md'; t=p.read_text(); stages=re.split(r'(?m)(?=^## Stage )',t)[1:]; errors=[]; diagrams=[]
req=['New Requirement','Existing Architecture','Architecture Change','Updated Diagram','What Remains Unchanged','New Failure Mode Introduced','Operational Signals','Security Impact','Cost Impact','Migration and Rollback','Interview Takeaway']
for i,s in enumerate(stages,1):
 for h in req:
  if f'### {h}\n' not in s: errors.append(f'stage {i}: missing {h}')
 m=re.search(r'```mermaid\n(.*?)```',s,re.S)
 if not m or len(set(re.findall(r'\b[A-Z][A-Za-z0-9_]+',m.group(1))))<2: errors.append(f'stage {i}: diagram lacks real component names')
 else:
  n=' '.join(re.sub(r'\d+','',m.group(1).lower()).split());
  if n in diagrams: errors.append(f'stage {i}: duplicate diagram')
  diagrams.append(n)
if len(stages)!=28: errors.append(f'expected 28 stages, found {len(stages)}')
if errors: print('\n'.join(errors));sys.exit(1)
print('Journey quality valid (28 evolving stages checked).')
