#!/usr/bin/env python3
"""Catch malformed Mermaid Markdown fences and empty/unknown diagrams."""
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]; errors=[]
for path in ROOT.glob('docs/**/*.md'):
    text=path.read_text(encoding='utf-8')
    starts=[m.start() for m in re.finditer(r'^```mermaid\s*$',text,re.M)]
    fences=list(re.finditer(r'^```\s*$',text,re.M))
    for start in starts:
        close=next((f for f in fences if f.start()>start),None)
        if not close: errors.append(f'{path.relative_to(ROOT)}: unclosed Mermaid fence'); continue
        body=text[start+len('```mermaid'):close.start()].strip()
        body=re.sub(r'^---\n.*?\n---\n','',body,flags=re.S)
        if not re.search(r'^(flowchart|graph|sequenceDiagram|stateDiagram|classDiagram|erDiagram|journey|gantt|pie|mindmap|timeline)\b',body,re.M):
            errors.append(f'{path.relative_to(ROOT)}: Mermaid block lacks a supported diagram declaration')
if errors: print('\n'.join(errors)); sys.exit(1)
print('Mermaid fences and declarations valid.')
