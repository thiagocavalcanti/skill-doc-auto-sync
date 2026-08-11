#!/usr/bin/env python3
"""
init_doc_tracking.py: Scans the repository for documentation files,
extracts potential topics based on Markdown headers, and generates
the tracked_docs.json manifest interactively.
"""

import os
import json
from pathlib import Path

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    MAGENTA = "\033[35m"

def find_markdown_files(root_dir):
    ignore_dirs = {".git", "node_modules", "vendor", ".venv", "venv", "dist", "build"}
    md_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs and not d.startswith('.')]
        for f in filenames:
            if f.endswith('.md'):
                md_files.append(Path(dirpath) / f)
                
    return md_files

def extract_topics_from_md(file_path):
    topics = []
    try:
        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        
        current_h1 = None
        for line in lines:
            line = line.strip()
            if line.startswith("# "):
                current_h1 = line[2:].strip()
                topic_id = current_h1.lower().replace(" ", "-").replace("/", "-")
                topics.append({
                    "id": topic_id,
                    "name": current_h1,
                    "version": 1,
                    "description": f"Documentation section for {current_h1}",
                    "match_patterns": ["*"] # Default broad match, user can refine
                })
            elif line.startswith("## "):
                h2 = line[3:].strip()
                topic_id = h2.lower().replace(" ", "-").replace("/", "-")
                topics.append({
                    "id": topic_id,
                    "name": f"{current_h1} - {h2}" if current_h1 else h2,
                    "version": 1,
                    "description": f"Subsection covering {h2}",
                    "match_patterns": ["*"]
                })
    except Exception as e:
        print(f"{Colors.YELLOW}Warning: Could not parse {file_path}: {e}{Colors.RESET}")
    return topics

def main():
    repo_root = Path.cwd()
    print(f"\n{Colors.BOLD}{Colors.CYAN}--- Document Auto-Sync Initialization ---{Colors.RESET}")
    print(f"Scanning {repo_root} for Markdown files...\n")
    
    md_files = find_markdown_files(repo_root)
    if not md_files:
        print(f"{Colors.YELLOW}No markdown files found to track.{Colors.RESET}")
        return

    tracked_files_data = []

    for i, md_file in enumerate(md_files):
        rel_path = md_file.relative_to(repo_root)
        print(f"{Colors.BOLD}{Colors.MAGENTA}[{i}] {rel_path}{Colors.RESET}")
        
    print("\n")
    choice = input(f"Enter the numbers of the files you want to track (comma separated), or 'all' to track all: ").strip()
    
    selected_indices = []
    if choice.lower() == 'all':
        selected_indices = list(range(len(md_files)))
    else:
        try:
            selected_indices = [int(x.strip()) for x in choice.split(",") if x.strip().isdigit()]
        except ValueError:
            print("Invalid input. Exiting.")
            return

    for idx in selected_indices:
        if 0 <= idx < len(md_files):
            md_file = md_files[idx]
            rel_path = str(md_file.relative_to(repo_root))
            print(f"\n{Colors.CYAN}Extracting topics from {rel_path}...{Colors.RESET}")
            extracted_topics = extract_topics_from_md(md_file)
            
            final_topics = []
            if not extracted_topics:
                # Provide a default topic if no headers found
                final_topics = [{
                    "id": "general-overview",
                    "name": "General Overview",
                    "version": 1,
                    "description": f"General documentation for {rel_path}",
                    "match_patterns": ["*"]
                }]
            else:
                print("Found the following topics:")
                for j, topic in enumerate(extracted_topics):
                    print(f"  [{j}] {topic['name']} (ID: {topic['id']})")
                
                t_choice = input(f"Enter topic numbers to track for {rel_path} (comma separated), or 'all': ").strip()
                if t_choice.lower() == 'all':
                    final_topics = extracted_topics
                else:
                    try:
                        t_indices = [int(x.strip()) for x in t_choice.split(",") if x.strip().isdigit()]
                        final_topics = [extracted_topics[t_idx] for t_idx in t_indices if 0 <= t_idx < len(extracted_topics)]
                    except ValueError:
                        print("Invalid input, skipping topics.")

            if final_topics:
                tracked_files_data.append({
                    "path": rel_path,
                    "topics": final_topics
                })

    if not tracked_files_data:
        print(f"{Colors.YELLOW}No topics selected. Manifest not created.{Colors.RESET}")
        return

    manifest_data = {
        "version": "1.0.0",
        "tracked_files": tracked_files_data
    }

    # Determine where to save tracked_docs.json
    # It should ideally live in .agents/skills/doc-auto-sync/
    skill_dir = repo_root / ".agents" / "skills" / "doc-auto-sync"
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    manifest_path = skill_dir / "tracked_docs.json"
    manifest_path.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}✔ Tracking manifest created at {manifest_path}{Colors.RESET}")
    print(f"{Colors.GREEN}doc-auto-sync is now active for this repository!{Colors.RESET}\n")

if __name__ == "__main__":
    main()
