import os

def read_file_list(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            return [line for line in lines if line]  # remove empty lines
    except FileNotFoundError:
        print("❌ 'Files List.txt' not found!")
        return []  
  
def create_files(base_path, file_list, handle_no_ext):
    for name in file_list:
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

        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, 'w') as f:
                pass  # just create empty file
            print(f"✅ Created: {file_path}")
        except Exception as e:
            print(f"❌ Error creating {name}: {e}")  


def main():
    print("--------File Generator.py--------")
    
    # read "File List.txt"
    file_list = read_file_list("Files List.txt")
    if not file_list:
      return
    
    # ask for out put path
    output_path = input("🏠 Enter the output path: ")
    if not os.path.exists(output_path):
      print("Output path does not exist.")
      return
    
    # ask for separate folder
    separate_folder = input("Do you want to create separate folder (y/n): ").lower().strip()
    if separate_folder == "y":
      folder_name = input("📂 Enter folder name: ").strip()
      output_path = os.path.join(output_path, folder_name)
      os.makedirs(output_path, exist_ok=True)
    
    
    # handle file without extensions (e.g. no .txt , .cpp , .py etc)
    handle_no_ext = input("⚡ Files without extension (skip/folder): ").lower().strip()
    if handle_no_ext not in ['skip', 'folder']:
                  handle_no_ext = 'skip'
    
    # if execution were successfull...              
    print("\n🚀 Generating files...\n")
    create_files(output_path, file_list, handle_no_ext)

    print(f"\n🎉 Done! -> Path -> {output_path}")              
           
if __name__ == "__main__":
     main()