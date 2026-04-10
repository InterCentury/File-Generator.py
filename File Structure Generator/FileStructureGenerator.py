#!/usr/bin/env python3
"""
File Structure Generator from ASCII Tree
Reads a text file containing a tree representation (like the output of `tree` command)
and recreates the folder/file structure on disk.
"""

import os
import sys
import re
from pathlib import Path

# ----------------------------------------------------------------------
# Configuration & User Prompts
# ----------------------------------------------------------------------

def ask_yes_no(prompt, default=None):
    """Ask a yes/no question. Returns True for yes, False for no."""
    prompt = prompt + " (y/n): "
    if default is not None:
        prompt = prompt.rstrip(": ") + f" [{default}]: "
    while True:
        answer = input(prompt).strip().lower()
        if not answer and default is not None:
            return default.lower() == 'y'
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        print("Please answer y or n.")

def ask_choice(prompt, options, default=None):
    """Ask user to choose from a list of options."""
    prompt = prompt + f" ({'/'.join(options)})"
    if default:
        prompt += f" [{default}]"
    prompt += ": "
    while True:
        answer = input(prompt).strip().lower()
        if not answer and default:
            return default
        if answer in options:
            return answer
        print(f"Please choose from {options}")

# ----------------------------------------------------------------------
# Filename sanitisation (Windows / Unix safe)
# ----------------------------------------------------------------------

INVALID_CHARS_PATTERN = re.compile(r'[<>:"/\\|?*\x00-\x1f]')

def sanitize_filename(name, remove_invalid=True, replace_with='_'):
    """
    Remove or replace characters that are invalid in filenames.
    If remove_invalid is False, raises ValueError when invalid chars found.
    """
    if not remove_invalid:
        if INVALID_CHARS_PATTERN.search(name):
            raise ValueError(f"Invalid characters in name: {name}")
        return name

    # Replace invalid characters
    sanitized = INVALID_CHARS_PATTERN.sub(replace_with, name)
    # Also strip leading/trailing spaces and dots (Windows doesn't like them)
    sanitized = sanitized.strip(' .')
    if not sanitized:
        sanitized = '_empty_'
    return sanitized

# ----------------------------------------------------------------------
# Tree parsing
# ----------------------------------------------------------------------

def parse_tree_line(line):
    """
    Parse a single line from the tree text.
    Returns (depth, node_name, is_folder) or None if line is empty.
    Depth = number of indentation levels (each level = 4 chars: "│   " or "    ")
    """
    line = line.rstrip('\n')
    if not line.strip():
        return None

    # Special case: first line (root) might have no prefix and no ├──/└──
    if '├──' not in line and '└──' not in line:
        # root line like "python-handbook/"
        node_name = line.strip()
        # Determine if folder: ends with '/'
        is_folder = node_name.endswith('/')
        if is_folder:
            node_name = node_name.rstrip('/')
        return (0, node_name, is_folder)

    # Find the position of the node marker
    marker_pos = -1
    marker = None
    for m in ('├──', '└──'):
        pos = line.find(m)
        if pos != -1:
            marker_pos = pos
            marker = m
            break

    if marker_pos == -1:
        # Should not happen, but fallback: treat whole line as node name
        return (0, line.strip(), False)

    prefix = line[:marker_pos]          # e.g. "│   " or "    " or "│   │   "
    node_name = line[marker_pos + len(marker):].strip()

    # Compute depth: each level occupies exactly 4 characters in prefix
    depth = len(prefix) // 4

    # Determine if folder: ends with '/'
    is_folder = node_name.endswith('/')
    if is_folder:
        node_name = node_name.rstrip('/')

    return (depth, node_name, is_folder)

def build_structure_from_tree(tree_text, files_without_ext_action='folder'):
    """
    Parse the tree text and return a list of (full_path, is_folder)
    relative to the root.
    """
    lines = tree_text.splitlines()
    if not lines:
        return []

    # Parse each line
    nodes = []
    for line in lines:
        parsed = parse_tree_line(line)
        if parsed:
            nodes.append(parsed)

    if not nodes:
        return []

    # The first node is the root
    root_name = nodes[0][1]
    root_is_folder = nodes[0][2]

    # Build hierarchy using depth stack
    # stack[depth] = Path object of the parent at that depth
    stack = {}
    result = []   # list of (relative_path, is_folder)

    for depth, name, is_folder in nodes:
        # Determine if this is a file (no trailing slash) and has no extension
        if not is_folder and '.' not in name:
            # No extension – decide based on user setting
            if files_without_ext_action == 'folder':
                is_folder = True
            else:  # 'skip' – skip this node entirely
                print(f"⚠️ Skipping file without extension: {name}")
                continue

        # Build full relative path
        if depth == 0:
            # Root
            current_path = Path(name)
        else:
            parent = stack.get(depth - 1)
            if parent is None:
                # Should not happen if depth is consistent
                print(f"⚠️ Orphan node at depth {depth}: {name}")
                continue
            current_path = parent / name

        # Store for later children
        if is_folder:
            stack[depth] = current_path
        else:
            # Files don't become parents, but we still keep stack for same depth
            # (we don't modify stack for files)
            pass

        result.append((current_path, is_folder))

    return result

# ----------------------------------------------------------------------
# File/folder creation
# ----------------------------------------------------------------------

def create_structure(items, base_path, sanitize_mode, skip_invalid):
    """
    Create all folders and files from the parsed structure.
    """
    created_count = 0
    for rel_path, is_folder in items:
        full_path = base_path / rel_path

        # Sanitise the final component of the path
        parent = full_path.parent
        name = full_path.name
        try:
            safe_name = sanitize_filename(name, remove_invalid=(sanitize_mode == 'remove'), replace_with='_')
        except ValueError:
            if skip_invalid:
                print(f"⏭️ Skipping (invalid name): {full_path}")
                continue
            else:
                raise

        if safe_name != name:
            print(f"🔧 Renamed: {name} -> {safe_name}")
        full_path = parent / safe_name

        try:
            if is_folder:
                full_path.mkdir(parents=True, exist_ok=True)
                print(f"📁 Created: {full_path}")
                created_count += 1
            else:
                # Ensure parent folder exists
                full_path.parent.mkdir(parents=True, exist_ok=True)
                # Create empty file
                full_path.touch(exist_ok=True)
                print(f"📄 Created: {full_path}")
                created_count += 1
        except Exception as e:
            print(f"❌ Error creating {full_path}: {e}")

    return created_count

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    print("=" * 60)
    print("        FILE STRUCTURE GENERATOR from ASCII TREE")
    print("=" * 60)

    # 1. Input file (default: "File Structure.txt" in script dir)
    script_dir = Path(__file__).parent
    default_input = script_dir / "File Structure.txt"
    input_path = input(f"📄 Path to tree file [{default_input}]: ").strip()
    if not input_path:
        input_path = default_input
    input_path = Path(input_path)

    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    tree_text = input_path.read_text(encoding='utf-8')

    # 2. Output root directory
    output_root = input("🏠 Enter the output root directory: ").strip()
    if not output_root:
        print("❌ No output directory provided.")
        sys.exit(1)
    output_root = Path(output_root).resolve()

    # 3. Ask for options
    create_separate_root = ask_yes_no("🦺 Create a separate folder for the root (i.e., use the tree's top-level name as a subfolder)", default='y')
    files_without_ext = ask_choice("⚡ Files without extension", ['folder', 'skip'], default='folder')
    skip_invalid = ask_yes_no("🚩 Skip files/folders with invalid name characters", default='n')
    sanitize_invalid = ask_yes_no("⚠️ Remove invalid characters from names (if no, will ask to skip)", default='y')
    sanitize_mode = 'remove' if sanitize_invalid else 'raise'

    # 4. Parse tree structure
    print("\n📊 Parsing tree structure...")
    items = build_structure_from_tree(tree_text, files_without_ext_action=files_without_ext)

    if not items:
        print("❌ No valid entries found in tree file.")
        sys.exit(1)

    # 5. Adjust for separate root folder if requested
    if create_separate_root and items:
        root_rel_path = items[0][0]  # first item is the root
        # Prepend that root name to all paths
        new_items = []
        for rel_path, is_folder in items:
            new_items.append((root_rel_path / rel_path, is_folder))
        items = new_items
        base_path = output_root
    else:
        # Use the root name directly as part of base path? No, we just create everything under output_root
        # The first item's rel_path is the root folder name.
        # We'll keep base_path = output_root and let the first folder be created inside it.
        base_path = output_root

    # 6. Create structure
    print("\n🚀 Generating files & folders...\n")
    created = create_structure(items, base_path, sanitize_mode, skip_invalid)

    print(f"\n🎉 Done! Created {created} items.")
    print(f"📂 Location: {base_path}")

if __name__ == "__main__":
    main()