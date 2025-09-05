# Zip Generator Script

## Overview
This Python script generates a `create_zip.py` script that can create a zip file containing all files from a specified input directory, preserving the directory hierarchy. The generated script embeds file contents directly in its code, allowing for easy recreation of the zip file without needing the original files.

## Features
- Recursively scans an input directory to collect all files and their contents.
- Handles both text and binary files (with UTF-8 encoding and error handling for binary files).
- Preserves directory structure, including empty directories.
- Generates a standalone `create_zip.py` script that creates a zip file with the specified name.
- Supports command-line arguments for input directory, output script name, and zip file name.

## Requirements
- Python 3.6+
- Standard libraries: `os`, `zipfile`, `pathlib`, `argparse`

## Installation
No additional installation is required beyond having Python installed, as the script uses only standard Python libraries.

## Usage
Run the script from the command line, providing the input directory and optional arguments for the output script name and zip file name.

```bash
python generate_create_zip.py <input_directory> [--output <output_script_name>] [--zip-name <zip_file_name>]
```

### Arguments
- `input_directory`: Path to the directory containing the files to be zipped.
- `--output` (optional): Name of the generated script (default: `create_zip.py`).
- `--zip-name` (optional): Name of the zip file to be created by the generated script (default: `output.zip`).

### Example
To generate a script that creates a zip file from a directory named `my_project`:

```bash
python generate_create_zip.py my_project --output create_my_zip.py --zip-name my_project.zip
```

This will:
1. Generate a `create_my_zip.py` script.
2. When `create_my_zip.py` is run, it will create `my_project.zip` containing all files from `my_project`, preserving the directory structure.

## How It Works
1. The script scans the input directory recursively, collecting file contents and noting empty directories.
2. For each file, it attempts to read the content as UTF-8 text. If that fails (e.g., for binary files), it reads as bytes and decodes with error handling.
3. It generates a `create_zip.py` script that includes:
   - A dictionary of file paths and their contents.
   - Code to create a zip file using `zipfile.ZipFile` with the specified name.
   - Logic to add empty directories to the zip file.
4. The generated script can be run independently to create the zip file.

## Notes
- Ensure the input directory exists and is accessible.
- Binary files are included but may have partial content loss if they contain non-UTF-8-compatible data.
- The generated `create_zip.py` script is standalone and does not require the original files to create the zip.

## License
This project is licensed under the MIT License.
