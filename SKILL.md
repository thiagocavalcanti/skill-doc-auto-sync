---
name: doc-auto-sync
description: "Automatic documentation tracking and topic-versioned sync system. Installs helper scripts to initialize doc tracking and perform pre-commit verification."
user-invocable: true
author: Thiago Cavalcanti
metadata:
  hermes:
    tags: [docs, git, sync, automation, tokens]
    category: productivity
---

# 📚 Documentation Auto-Sync & Topic Versioning Skill

This skill guarantees that project documentation remains **100% synchronized with code changes** while minimizing LLM token consumption via targeted topic updates.

## 🚀 How to Use

When this skill is invoked or you are instructed to set up documentation tracking:

### Step 1: Initialize Tracking (First Run)
If the project does not have a `.agents/skills/doc-auto-sync/tracked_docs.json` file, you must initialize the tracking system.
Run the initialization script (installed by this skill into the target repository):
```bash
python3 .agents/skills/doc-auto-sync/scripts/init_doc_tracking.py
```
*Note: This script will scan for Markdown files, suggest topics based on headings, and interactively prompt the user (or you, the agent) to confirm which documents to track, generating the `tracked_docs.json` manifest.*

### Step 2: Pre-Commit Documentation Sync (Continuous)
Before drafting **any** Git commit in a tracked repository, you **MUST** run the doc sync evaluator:
```bash
python3 .agents/skills/doc-auto-sync/scripts/check_doc_sync.py
```

#### Decision Tree based on output:
- **If STALE topics are detected**:
  1. Read ONLY the specific sections of the documentation files corresponding to the STALE topic IDs.
  2. Update the Markdown documentation to accurately reflect the staged code changes.
  3. The `check_doc_sync.py` script will have informed you of the current version. Increment that topic `version` counter by `1` in `tracked_docs.json`.
  4. Stage the updated documentation file AND `tracked_docs.json`.
- **If UNTRACKED docs are detected**:
  - The script will warn you if new or heavily modified `.md` files are staged but not tracked. Prompt the user or automatically add them as new topics to `tracked_docs.json`.
- **If NO STALE topics are detected**:
  - Skip documentation edits completely to save tokens and maintain commit speed.
