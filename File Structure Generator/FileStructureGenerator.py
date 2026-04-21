"""
Simple File Structure Generator from ASCII Tree
Reads tree from 'File Structure.txt' and creates folders/files on disk.
"""

import re
from pathlib import Path

# ----------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------

def ask_yes_no(prompt, default='y'):
    """Simple yes/no question."""
    default_display = 'Y/n' if default.lower() == 'y' else 'y/N'
    answer = input(f"{prompt} ({default_display}): ").strip().lower()
    if not answer:
        return default.lower() == 'y'
    return answer in ('y', 'yes')

def sanitize_filename(name):
    """Remove invalid characters from filename."""
    invalid_chars = r'[<>:"/\\|?*]'
    name = re.sub(invalid_chars, '_', name)
    name = name.strip(' .')
    return name if name else '_empty_'

def parse_tree_line(line):
    """Parse a tree line and return (depth, name, is_folder).

    Depth is derived from the byte-column where the name starts.
    A root-level entry (no tree prefix) has depth 0.
    Each additional level adds 4 columns (│   or ├── or └── patterns).
    """
    line = line.rstrip('\n')
    if not line.strip():
        return None

    # Strip the trailing name from the line; everything before it is the prefix.
    # Tree connector characters: │ ├ └ ─ and plain spaces.
    match = re.match(r'^((?:[│├└─\s])*)', line)
    prefix = match.group(1) if match else ''
    name = line[len(prefix):].strip()

    if not name:
        return None

    # Depth = how many 4-column "slots" the prefix occupies.
    # Replace tree box-drawing chars with spaces so we can measure width.
    # Each box-drawing character is 1 column wide.
    prefix_as_spaces = re.sub(r'[│├└─]', ' ', prefix)
    col = len(prefix_as_spaces)

    # Root items sit at column 0; each indent level is 4 columns.
    depth = col // 4

    # Check if it's a folder (ends with /)
    is_folder = name.endswith('/')
    name = name.rstrip('/')

    return (depth, name, is_folder)

def build_structure(tree_text, files_without_ext='skip'):
    """Parse tree text and build list of (path, is_folder)."""
    lines = tree_text.splitlines()
    if not lines:
        return []

    # Parse all lines
    nodes = []
    for line in lines:
        parsed = parse_tree_line(line)
        if parsed:
            nodes.append(parsed)

    if not nodes:
        return []

    # Build hierarchy using stack
    stack = {}
    result = []

    for depth, name, is_folder in nodes:
        # Handle files without extension
        if not is_folder and '.' not in name:
            if files_without_ext == 'folder':
                is_folder = True
            else:  # skip
                print(f"⚠️ Skipping: {name}")
                continue

        # Build path
        if depth == 0:
            current_path = Path(name)
        else:
            parent = stack.get(depth - 1)
            if parent is None:
                # Fallback: walk back up the stack to find the nearest ancestor
                for d in range(depth - 1, -1, -1):
                    if d in stack:
                        parent = stack[d]
                        break
            if parent is None:
                print(f"⚠️ Could not find parent for: {name} (depth {depth}), skipping")
                continue
            current_path = parent / name

        if is_folder:
            stack[depth] = current_path
            # Clear any stale deeper entries so they don't bleed into siblings
            stale = [k for k in stack if k > depth]
            for k in stale:
                del stack[k]

        result.append((current_path, is_folder))

    return result

def create_structure(items, base_path, sanitize_names, skip_invalid):
    """Create all folders and files."""
    created = 0

    for rel_path, is_folder in items:
        full_path = base_path / rel_path

        # Sanitize name if requested
        if sanitize_names:
            safe_name = sanitize_filename(full_path.name)
            if safe_name != full_path.name:
                print(f"🔧 Renamed: {full_path.name} -> {safe_name}")
            full_path = full_path.parent / safe_name

        try:
            if is_folder:
                full_path.mkdir(parents=True, exist_ok=True)
                print(f"📁 Created: {full_path}")
                created += 1
            else:
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.touch(exist_ok=True)
                print(f"✅ Created: {full_path}")
                created += 1
        except Exception as e:
            if skip_invalid:
                print(f"⏭️ Skipped: {full_path}")
            else:
                print(f"❌ Error: {full_path} - {e}")

    return created

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    print("-" * 50)
    print("File Structure Generator")
    print("-" * 50)

    # Get script directory and default tree file
    script_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd()
    tree_file = script_dir / "File Structure.txt"

    # Check if tree file exists
    if not tree_file.exists():
        print(f"❌ Error: '{tree_file}' not found!")
        print("   Please create 'File Structure.txt' with your tree structure")
        return

    # Read the tree structure
    tree_text = tree_file.read_text(encoding='utf-8')

    # Get output path
    output_path = input("🏠 Enter the output path: ").strip()
    if not output_path:
        print("❌ No output directory provided")
        return
    output_path = Path(output_path).resolve()

    # Ask for options
    create_separate = ask_yes_no("🦺 Do you want to create separate folder", default='y')
    if create_separate:
        folder_name = input("📂 Enter folder name: ").strip()
        if folder_name:
            output_path = output_path / folder_name

    files_without_ext = input("⚡ Files without extension (skip/folder): ").strip().lower()
    if files_without_ext not in ['skip', 'folder']:
        files_without_ext = 'skip'

    skip_invalid = ask_yes_no("🚩 Skip files with invalid name", default='y')
    sanitize_names = ask_yes_no("⚠️ Remove invalid character from file name", default='y')

    # Generate structure
    print("\n🚀 Generating files...\n")

    items = build_structure(tree_text, files_without_ext)
    if not items:
        print("❌ No valid structure found in File Structure.txt")
        return

    created = create_structure(items, output_path, sanitize_names, skip_invalid)

    print(f"\n🎉 Done! -> Path -> {output_path}")

if __name__ == "__main__":
    main()