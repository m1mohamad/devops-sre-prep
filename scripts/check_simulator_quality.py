#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
import re,sys
p=Path(__file__).resolve().parents[1]/'docs/simulator/index.md'; chunks=re.split(r'(?m)(?=^# Scenario )',p.read_text())[1:]; errors=[]
for heading in ['Architecture','Initial Symptoms','Investigation Timeline','Prevention','SLO and Alert Improvements','What Would a Staff Engineer Change?']:
 seen=defaultdict(list)
 for i,c in enumerate(chunks,1):
  m=re.search(rf'^## {re.escape(heading)}\n\n(.*?)(?=\n## |\n# |\Z)',c,re.M|re.S)
  if not m: errors.append(f'scenario {i}: missing {heading}'); continue
  v=' '.join(m.group(1).lower().split())
  seen[v].append(i)
 for v,where in seen.items():
  if len(where)>1: errors.append(f'identical {heading}: scenarios {where}')
if len(chunks)!=8: errors.append(f'expected 8 scenarios, found {len(chunks)}')
if errors: print('\n'.join(errors));sys.exit(1)
print('Simulator quality valid (8 distinct scenarios checked).')
