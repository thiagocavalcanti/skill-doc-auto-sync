# 📚 doc-auto-sync

[![skills.sh](https://skills.sh/b/thiagocavalcanti/skill-doc-auto-sync)](https://skills.sh/thiagocavalcanti/skill-doc-auto-sync)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

> **Token-optimized, topic-versioned documentation sync for AI coding agents.**

`doc-auto-sync` is an Agent Skill designed to keep project documentation 100% synchronized with codebase evolution without overwhelming LLM context windows.

---

## ⚡ Quick Start

### Installation

Install this skill into any repository using the standard skills CLI:

```bash
npx -y skills@latest add thiagocavalcanti/skill-doc-auto-sync
```

This provisions the skill and helper scripts into your project's `.agents/skills/doc-auto-sync/` directory.

---

## ✨ Features

- **Smart Discovery**: Automatically scans repository Markdown files and extracts section headers as trackable topics.
- **Topic Versioning**: Increments granular version counters in `tracked_docs.json` so agents only re-read stale documentation topics.
- **Diff-Aware Pre-Commit Checks**: Evaluates staged git changes against defined match patterns before commits are made.
- **Untracked Doc Alerts**: Detects newly added or modified Markdown files and prompts the agent or user to track them.
- **Token Efficiency**: Prevents LLMs from reading full documentation files when only specific topics need updating.

---

## 🛠️ Usage

### 1. Initialization (First Run)

Run the interactive discovery script to scan your project for Markdown files and generate `.agents/skills/doc-auto-sync/tracked_docs.json`:

```bash
python3 .agents/skills/doc-auto-sync/scripts/init_doc_tracking.py
```

The script will present discovered files and sections, letting you select which topics to track.

### 2. Pre-Commit Verification (Continuous)

Before creating a Git commit, run the sync evaluator:

```bash
python3 .agents/skills/doc-auto-sync/scripts/check_doc_sync.py
```

- **If stale topics are detected**: The script outputs the specific topic IDs, paths, and current version numbers. Update only those sections in the documentation, increment their version counter in `tracked_docs.json`, and stage the changes.
- **If untracked `.md` files are detected**: The script alerts you to add them to `tracked_docs.json`.
- **If all documentation is up to date**: You save context tokens and proceed straight to commit!

---

## 📄 Manifest Structure (`tracked_docs.json`)

`doc-auto-sync` maintains a manifest structured as follows:

```json
{
  "version": "1.0.0",
  "tracked_files": [
    {
      "path": "README.md",
      "topics": [
        {
          "id": "general-overview",
          "name": "General Overview & Setup",
          "version": 1,
          "description": "Project overview and installation steps",
          "match_patterns": ["src/*", "package.json"]
        }
      ]
    }
  ]
}
```

---

## 💰 Token & Cost Savings Simulation

Without `doc-auto-sync`, an AI agent checking documentation freshness before every commit must read all repository documentation files to determine if anything is outdated.
`doc-auto-sync` replaces this brute-force reading with a zero-token local script check (`check_doc_sync.py`).
The script evaluates staged git diffs against `tracked_docs.json` topic patterns in milliseconds.
When a code change matches a tracked topic, the AI agent is instructed to read only the specific ~1k token topic section rather than entire documentation files.

### Savings Matrix over 100 Commits

The table below compares full-document inspection against `doc-auto-sync` over 100 commits (assuming ~10% of commits touch tracked code patterns, reading ~1k tokens per match).
Estimated costs are calculated at a standard rate of **$3.00 per 1M input tokens**.

| Number of Docs | Size per Doc | Total Docs Size | Unoptimized Tokens (100 Commits) | Unoptimized Cost | `doc-auto-sync` Tokens (100 Commits) | `doc-auto-sync` Cost | Savings (%) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **1k tokens** | 1,000 tokens | 100,000 | $0.30 | 10,000 | $0.03 | **90.0%** |
| **1** | **10k tokens** | 10,000 tokens | 1,000,000 | $3.00 | 10,000 | $0.03 | **99.0%** |
| **1** | **100k tokens** | 100,000 tokens | 10,000,000 | $30.00 | 10,000 | $0.03 | **99.9%** |
| **10** | **1k tokens** | 10,000 tokens | 1,000,000 | $3.00 | 10,000 | $0.03 | **99.0%** |
| **10** | **10k tokens** | 100,000 tokens | 10,000,000 | $30.00 | 10,000 | $0.03 | **99.9%** |
| **10** | **100k tokens** | 1,000,000 tokens | 100,000,000 | $300.00 | 10,000 | $0.03 | **99.99%** |
| **100** | **1k tokens** | 100,000 tokens | 10,000,000 | $30.00 | 10,000 | $0.03 | **99.9%** |
| **100** | **10k tokens** | 1,000,000 tokens | 100,000,000 | $300.00 | 10,000 | $0.03 | **99.99%** |
| **100** | **100k tokens** | 10,000,000 tokens | 1,000,000,000 | $3,000.00 | 10,000 | $0.03 | **99.999%** |

### Key Takeaways

By shifting documentation diff evaluation from the LLM context window to a deterministic local script, `doc-auto-sync` eliminates redundant context loading.
As repository size and documentation depth grow, token savings scale exponentially while maintaining 100% documentation freshness.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check out the [issues page](https://github.com/thiagocavalcanti/skill-doc-auto-sync/issues).

---

## 📜 License

Distributed under the MIT License.
