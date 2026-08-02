#!/usr/bin/env python3
"""Reject structural omissions and duplicated boilerplate in numbered study notes."""
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher
import re, sys
ROOT=Path(__file__).resolve().parents[1]
REQ=['30-Second Answer','Mental Model','Architecture Diagram','Core Components','How It Actually Works','Production Design','Failure Modes','Troubleshooting Procedure','Security Considerations','Scaling and Cost','Trade-offs','Lead-Level Follow-ups','My Experience Prompt','Recall Check','Related Notes','Further Reading']
GENERIC=['component x owns stage','inspect state, events, latency, permissions, and capacity','previous stage --> requirement --> controlled change --> feedback']
def norm(s):
 s=re.sub(r'\*+|_+|\d+',' ',s.lower()); s=re.sub(r'\b[a-z]\w*\s*(?=-->|---|==>)','node ',s); return ' '.join(s.split())
def blocks(t,kind='paragraph'):
 if kind=='diagram': return re.findall(r'```mermaid\n(.*?)```',t,re.S)
 return [x for x in re.split(r'\n\s*\n',t) if len(norm(x).split())>=18 and not x.startswith(('#','```','|'))]
errors=[]; seen=defaultdict(list); diagrams=[]
priority={'kubernetes':set(f'{i:02d}' for i in range(1,11)),'iac':{'02','03','04','05'},'cicd':{'02','03','04','05'},'aws':{'03','04','05','07'},'observability':{'01','02','03','04','05'}}
new_tracks={'linux-networking','scripting','go','databases','helm','container-security','cost-performance','leadership'}
for p in sorted((ROOT/'docs/study').glob('*/[0-9][0-9]-*.md')):
 if p.parent.name not in new_tracks and p.name[:2] not in priority.get(p.parent.name,set()): continue
 t=p.read_text(); heads=re.findall(r'^## (.+)$',t,re.M)
 for h in set(heads):
  if heads.count(h)>1: errors.append(f'{p.relative_to(ROOT)}: duplicate heading {h}')
 for h in REQ:
  if f'## {h}\n' not in t: errors.append(f'{p.relative_to(ROOT)}: missing {h}')
 for phrase in GENERIC:
  if phrase in t.lower(): errors.append(f'{p.relative_to(ROOT)}: forbidden generic template phrase')
 for b in blocks(t): seen[norm(b)].append(p)
 for d in blocks(t,'diagram'): diagrams.append((p,norm(d)))
for b,ps in seen.items():
 if len(set(ps))>=40: errors.append(f'repeated mechanism paragraph in {len(set(ps))} notes: {b[:80]}')
for i,(a,x) in enumerate(diagrams):
 for b,y in diagrams[i+1:]:
  if a.parent!=b.parent and len(x)>60 and SequenceMatcher(None,x,y).ratio()>.99: errors.append(f'near-identical diagrams: {a.relative_to(ROOT)}, {b.relative_to(ROOT)}')
if errors: print('\n'.join(dict.fromkeys(errors))); sys.exit(1)
print(f'Study similarity valid ({len(diagrams)} diagrams checked).')
