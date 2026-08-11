#!/usr/bin/env python3
"""
check_doc_sync.py: Evaluates staged or modified files against tracked_docs.json match patterns.
Identifies stale documentation topics requiring updates and checks for new untracked Markdown files.
"""

import sys
import os
import json
import fnmatch
import subprocess
from pathlib import Path

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"

def get_git_changed_files():
    # Staged files first
    res = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True)
    files = [f.strip() for f in res.stdout.splitlines() if f.strip()]
    if not files:
        # Fallback to unstaged modified files
        res = subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True)
        files = [f.strip() for f in res.stdout.splitlines() if f.strip()]
    return files

def main():
    # Try script location parent repo directory first (.agents/skills/doc-auto-sync/scripts/ -> repo_root)
    script_based_repo = Path(__file__).resolve().parents[3]
    manifest_path = script_based_repo / ".agents" / "skills" / "doc-auto-sync" / "tracked_docs.json"

    if not manifest_path.exists():
        # Fall back to CWD
        repo_dir = Path.cwd()
        manifest_path = repo_dir / ".agents" / "skills" / "doc-auto-sync" / "tracked_docs.json"

    if not manifest_path.exists():
        print(f"{Colors.YELLOW}⚠ Manifest file not found at {manifest_path}. Run init_doc_tracking.py first.{Colors.RESET}")
        sys.exit(0)

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}✖ Error reading manifest: {e}{Colors.RESET}")
        sys.exit(1)

    changed_files = get_git_changed_files()
    if not changed_files:
        print(f"{Colors.GREEN}✔ No changed files detected in git working tree.{Colors.RESET}")
        sys.exit(0)

    print(f"\n{Colors.BOLD}{Colors.CYAN}Checking documentation sync for {len(changed_files)} changed file(s)...{Colors.RESET}\n")

    stale_topics = []
    tracked_doc_paths = set()

    for file_entry in manifest.get("tracked_files", []):
        doc_path = file_entry.get("path")
        tracked_doc_paths.add(doc_path)
        for topic in file_entry.get("topics", []):
            topic_id = topic.get("id")
            topic_name = topic.get("name")
            version = topic.get("version")
            patterns = topic.get("match_patterns", [])

            is_match = False
            for changed in changed_files:
                for pat in patterns:
                    if fnmatch.fnmatch(changed, pat) or pat in changed:
                        is_match = True
                        break
                if is_match:
                    break

            if is_match:
                stale_topics.append({
                    "doc_path": doc_path,
                    "topic_id": topic_id,
                    "topic_name": topic_name,
                    "version": version,
                    "description": topic.get("description")
                })

    # Check for untracked markdown files in the commit
    untracked_md_files = []
    for f in changed_files:
        if f.endswith('.md') and f not in tracked_doc_paths:
            untracked_md_files.append(f)

    if stale_topics:
        print(f"{Colors.BOLD}{Colors.YELLOW}⚠ Stale Documentation Topics Detected ({len(stale_topics)}):{Colors.RESET}")
        for t in stale_topics:
            print(f"  • {Colors.BOLD}[{t['doc_path']}]{Colors.RESET} {Colors.CYAN}{t['topic_name']}{Colors.RESET} (Topic ID: {t['topic_id']} | Version: v{t['version']})")
            print(f"    {Colors.DIM}Description: {t['description']}{Colors.RESET}")
        print(f"\n{Colors.MAGENTA}Action Required:{Colors.RESET} Update the relevant sections in {set(t['doc_path'] for t in stale_topics)} and bump topic version in tracked_docs.json before commit.\n")
    else:
        print(f"{Colors.GREEN}✔ Existing documentation topics are up to date. (Tokens saved!){Colors.RESET}")

    if untracked_md_files:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}⚠ Untracked Documentation Files Modified:{Colors.RESET}")
        for umd in untracked_md_files:
            print(f"  • {Colors.YELLOW}{umd}{Colors.RESET}")
        print(f"\n{Colors.MAGENTA}Action Required:{Colors.RESET} Consider adding these files to .agents/skills/doc-auto-sync/tracked_docs.json if they need tracking.\n")

if __name__ == "__main__":
    main()
