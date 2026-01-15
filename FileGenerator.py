# Greetings from github.com/InterCentury 😄

import os

def read_file_list(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
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
            else:
                # if skip = n → always clean (safe mode)
                cleaned = clean_name(name)
                print(f"⚠️ Cleaned: {name} -> {cleaned}")
                name = cleaned

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

        try:
            with open(file_path, 'w') as f:
                pass
            print(f"✅ Created: {file_path}")
        except Exception as e:
            print(f"❌ Error creating {name}: {e}")


def main():
    print("--------File Generator.py--------")
    
    file_list = read_file_list("Files List.txt")
    if not file_list:
        return
    
    output_path = input("🏠 Enter the output path: ").strip()
    if not os.path.exists(output_path):
        print("❌ Output path does not exist.")
        return
    
    separate_folder = input("🦺 Do you want to create separate folder (y/n): ").lower().strip()
    if separate_folder == "y":
        folder_name = input("📂 Enter folder name: ").strip()
        output_path = os.path.join(output_path, folder_name)
        os.makedirs(output_path, exist_ok=True)
    
    handle_no_ext = input("⚡ Files without extension (skip/folder): ").lower().strip()
    if handle_no_ext not in ['skip', 'folder']:
        handle_no_ext = 'skip'

    
    skip_invalid = input("🚩 Skip files with invalid name (y/n): ").lower().strip()
    clean_invalid = input("⚠️ Remove invalid character from file name (y/n): ").lower().strip()

    print("\n🚀 Generating files...\n")
    create_files(output_path, file_list, handle_no_ext, skip_invalid, clean_invalid)

    print(f"\n🎉 Done! -> Path -> {output_path}")              


if __name__ == "__main__":
    main()