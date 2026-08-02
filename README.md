# DevOps & SRE Preparation Handbook

A portable, Markdown-first handbook for learning platform engineering, DevOps, and site reliability engineering.

## Read online

Browse the published handbook on [GitHub Pages](https://m1mohamad.github.io/devops-sre-prep/).

## Open as an Obsidian vault

1. Clone this repository.
2. In Obsidian, select **Open folder as vault** and choose the repository root.
3. Begin with [START-HERE.md](START-HERE.md).

The checked-in `.obsidian/app.json` keeps links portable. Personal workspace state, caches, trash, Python bytecode, and the generated MkDocs site are ignored.

## Preview locally with MkDocs

```bash
python -m pip install -r requirements.txt
mkdocs serve
```

Then open `http://127.0.0.1:8000/`. To run the same strict build used in CI:

```bash
mkdocs build --strict
```
