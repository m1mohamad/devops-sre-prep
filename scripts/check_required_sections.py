#!/usr/bin/env python3
"""Validate the recall-note contract for numbered topical study notes."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
required = ['30-Second Answer','Mental Model','Why It Exists','How It Works','Production Architecture','Failure Modes','Trade-offs','Lead-Level Follow-ups','My Experience Prompt','Recall Check','Related Notes']
errors=[]
for path in sorted((ROOT/'docs/study').glob('*/[0-9][0-9]-*.md')):
    if path.parent.name == 'interview':
        continue
    text=path.read_text(encoding='utf-8')
    if not text.startswith('---\n') or '\ntags:' not in text or '\naliases:' not in text:
        errors.append(f'{path.relative_to(ROOT)}: incomplete YAML front matter')
    for heading in required:
        if f'## {heading}\n' not in text:
            errors.append(f'{path.relative_to(ROOT)}: missing {heading!r}')
    if text.count('```mermaid') < 1:
        errors.append(f'{path.relative_to(ROOT)}: missing Mermaid mental model')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('Study-note structure valid.')
