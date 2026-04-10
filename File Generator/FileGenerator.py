
# Greetings from github.com/InterCentury 😄

import os
import sys

def read_file_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip().replace('\ufeff', '') for line in f.readlines()]
            return [line for line in lines if line]
    except FileNotFoundError:
        print("❌ 'Files List.txt' not found!")
        return []  


def clean_name(name):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    return name


def has_invalid_chars(name):
    invalid_chars = '<>:"/\\|?*'
    return any(char in name for char in invalid_chars)


def create_files(base_path, file_list, handle_no_ext, skip_invalid, clean_invalid):
    for name in file_list:

        # 🚩 Handle invalid names
        if has_invalid_chars(name):
            if skip_invalid == 'y':
                print(f"🚩 Skipped (invalid name): {name}")
                continue
            elif clean_invalid == 'y':
                cleaned = clean_name(name)
                if not cleaned:
                    print(f"🚩 Skipped (empty after cleaning): {name}")
                    continue
                print(f"⚠️ Cleaned: {name} -> {cleaned}")
                name = cleaned
            else:
                print(f"🚩 Skipped (invalid name, no clean): {name}")
                continue

        # Handle files without extension
        if '.' not in name:
            if handle_no_ext == 'skip':
                print(f"⚠️ Skipped (no extension): {name}")
                continue
            elif handle_no_ext == 'folder':
                folder_path = os.path.join(base_path, name)
                os.makedirs(folder_path, exist_ok=True)
                print(f"📁 Folder created: {folder_path}")
                continue

        file_path = os.path.join(base_path, name)

        # Safe directory creation
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        # Avoid overwriting existing files
        if os.path.exists(file_path):
            print(f"⚠️ Already exists: {file_path}")
            continue

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                pass
            print(f"✅ Created: {file_path}")
        except Exception as e:
            print(f"❌ Error creating {name}: {e}")


def main():
    print("--------File Generator.py--------")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files_list_path = os.path.join(script_dir, "Files List.txt")
    
    file_list = read_file_list(files_list_path)
    if not file_list:
        return
      
    # initialize output path
    output_path = input("🏠 Enter the output path: ").strip()
    if not os.path.exists(output_path):
        print("❌ Output path does not exist.")
        return
      
    # ask user for separate folder 
    separate_folder = input("🦺 Do you want to create separate folder (y/n): ").lower().strip()
    if separate_folder == "y":
        folder_name = input("📂 Enter folder name: ").strip()
        output_path = os.path.join(output_path, folder_name)
        os.makedirs(output_path, exist_ok=True)
        
    # ask user how to handle files without extension
    handle_no_ext = input("⚡ Files without extension (skip/folder): ").lower().strip()
    if handle_no_ext not in ['skip', 'folder']:
        handle_no_ext = 'skip'

    # invalid handling options
    skip_invalid = input("🚩 Skip files with invalid name (y/n): ").lower().strip()
    clean_invalid = input("⚠️ Remove invalid character from file name (y/n): ").lower().strip()
    
    # Execution start
    print("\n🚀 Generating files...\n")
    create_files(output_path, file_list, handle_no_ext, skip_invalid, clean_invalid)

    print(f"\n🎉 Done! -> Path -> {output_path}")              


if __name__ == "__main__":
    main()