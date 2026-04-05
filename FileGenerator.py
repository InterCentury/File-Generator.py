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



if __name__ == "__main__":
  main()