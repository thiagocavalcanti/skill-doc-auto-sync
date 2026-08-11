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

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check out the [issues page](https://github.com/thiagocavalcanti/skill-doc-auto-sync/issues).

---

## 📜 License

Distributed under the MIT License.
