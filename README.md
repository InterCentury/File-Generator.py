

# 📄 File Generator.py

A simple Python-based tool to generate multiple files instantly from a predefined list.

---

## 🚀 Features

* Generate unlimited files in one run
* Supports any file type (`.py`, `.txt`, `.json`, etc.)
* Optional folder creation for organized output
* Minimal and fast CLI (TUI-style interaction)
* 🚩 Option to skip files with invalid names
* ⚠️ Option to automatically sanitize invalid filenames
* 🛡️ Fail-safe mechanism to prevent crashes on Windows
* 📁 Automatic nested folder creation from file paths

---

## 📁 Project Structure

```
File-Generator.py/
│
├── FileGenerator.py     # Main script
├── Files List.txt       # List of file names to generate
└── README.md            # Documentation
```

---

## ⚙️ How It Works

1. Add file names to `Files List.txt`

   Example:

   ```
   test.py
   notes.txt
   config.json
   script.js
   invalid*file?.txt
   folder1
   nested/file2.py
   ```

2. Run the script:

   ```
   python FileGenerator.py
   ```

3. Follow the prompts:

   ```
   🏠 Enter output path: C:\files\
   🦺  Do you want to create separate folder (y/n): y
   📂 Enter folder name: generated_files
   ⚡ Files without extension (skip/folder): folder
   🚩 Skip files with invalid name (y/n): n
   ⚠️ Remove invalid character from file name (y/n): y
   ```

4. Done ✅ — all files will be created automatically.

---

## 💡 Example Output

```
C:\files\generated_files\
│
├── test.py
├── notes.txt
├── config.json
├── script.js
├── invalidfile.txt   # cleaned automatically
└── nested\
    └── file2.py
```

---

## 🧠 Use Cases

* Quickly scaffold project files
* Create test datasets
* Batch file creation for experiments
* Organize coding practice files
* Generate structured project folders instantly

---

## ⚠️ Notes

* Make sure the output path exists
* Empty lines in `Files List.txt` will be ignored
* File names without extensions can be skipped or treated as folders
* 🚫 Windows does not support characters like `< > : " / \ | ? *`
* ⚠️ Invalid filenames can be skipped or automatically cleaned
* Duplicate file names may overwrite existing files

