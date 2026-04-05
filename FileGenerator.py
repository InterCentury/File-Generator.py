import os

def read_file_list(file_path):
  
  
def create_files(base_path, file_list, handle_no_ext):
  


def main():
print("--------File Generator.py--------")

# read "File List.txt"
file_list = read_file_list("Files List.txt")
if not file_list:
  return

# ask for out put path
output_path = input("Enter the output path: ")
if not os.path.exists(output_path):
  print("Output path does not exist.")
  return

# ask for separate folder
separate_folder = input("Do you want to create separate folder (y/n): ").lower().strip()

if separate_folder == "y":
  folder_name = input("Enter folder name: ").strip()
  output_path = os.path.join(output_path, folder_name)
  os.makedirs(output_path, exist_ok=True)

if __name__ == "__main__":
  main()