# DevOps and SRE Interview Prep

This repository is a platform engineering handbook and interview-preparation vault. It brings together production-focused study notes, architecture examples, interview questions, incident simulations, and an engineering journey for DevOps, SRE, and platform engineering practice.

## Read online

The MkDocs site is published on [GitHub Pages](https://m1mohamad.github.io/devops-sre-prep/).

## Use with Obsidian

1. Clone the repository.
2. In Obsidian, select **Open folder as vault**.
3. Choose the repository root, not only the `docs/` directory, so Obsidian loads the tracked `.obsidian` configuration.
4. Open [START-HERE.md](START-HERE.md) and begin with the interview dashboard or seven-day study plan.

For one connected overview, study the [Core Path — End-to-End Platform](docs/study/core-path/index.md).

The notes use standard relative Markdown links, so Graph View and backlinks work without a community plugin.

## Run MkDocs locally

Create a virtual environment, install the pinned project requirements, and start the development server:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

Then open `http://127.0.0.1:8000/`. To validate a production build instead, run `mkdocs build --strict`.
