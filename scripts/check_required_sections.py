#!/usr/bin/env python3
"""Validate the required production-study note contract."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
required=['30-Second Answer','Mental Model','Architecture Diagram','Core Components','How It Actually Works','Production Design','Failure Modes','Troubleshooting Procedure','Security Considerations','Scaling and Cost','Trade-offs','Lead-Level Follow-ups','My Experience Prompt','Recall Check','Related Notes','Further Reading']
errors=[]
priority={'kubernetes':set(f'{i:02d}' for i in range(1,11)),'iac':{'02','03','04','05'},'cicd':{'02','03','04','05'},'aws':{'03','04','05','07'},'observability':{'01','02','03','04','05'}}
new_tracks={'linux-networking','scripting','go','databases','helm','container-security','cost-performance','leadership'}
for path in sorted((ROOT/'docs/study').glob('*/[0-9][0-9]-*.md')):
 if path.parent.name not in new_tracks and path.name[:2] not in priority.get(path.parent.name,set()): continue
 text=path.read_text(encoding='utf-8')
 if not text.startswith('---\n') or '\ntitle:' not in text or '\ntags:' not in text or '\naliases:' not in text: errors.append(f'{path.relative_to(ROOT)}: incomplete YAML front matter')
 for heading in required:
  if f'## {heading}\n' not in text: errors.append(f'{path.relative_to(ROOT)}: missing {heading!r}')
 if text.count('```mermaid')<1: errors.append(f'{path.relative_to(ROOT)}: missing Mermaid diagram')
if errors: print('\n'.join(errors));sys.exit(1)
print('Study-note structure valid.')
