import os
import zipfile
from pathlib import Path
import argparse

def generate_create_zip_script(input_dir, output_file="create_zip.py", zip_name="output.zip"):
    """
    Generate a create_zip.py script that includes all files from the input directory
    with their contents and preserves the directory hierarchy.
    """
    input_dir = Path(input_dir).resolve()
    if not input_dir.is_dir():
        raise ValueError(f"Input path {input_dir} is not a directory")

    # Collect all files and their contents
    files_dict = {}
    empty_dirs = []
    
    # Walk through the directory
    for root, dirs, files in os.walk(input_dir):
        rel_root = Path(root).relative_to(input_dir)
        
        # Collect empty directories
        if not files and not dirs:
            empty_dirs.append(str(rel_root))
        
        # Collect files and their contents
        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(input_dir)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Handle binary files by reading as bytes and converting to string representation
                with open(file_path, 'rb') as f:
                    content = f.read().decode('utf-8', errors='ignore')
            files_dict[str(rel_path)] = content

    # Generate the create_zip.py script content
    script_content = """import os
import zipfile
from pathlib import Path

def create_zip():
    # Define project structure
    files = {
"""
    
    # Add file contents to the script
    for file_path, content in files_dict.items():
        # Escape triple quotes in content to avoid breaking the Python string
        content = content.replace('"""', '\\"\\"\\"')
        script_content += f'        "{file_path}": """{content}""",\n'

    script_content += """    }

    # Create zip file
    with zipfile.ZipFile("{zip_name}", "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path, content in files.items():
            zipf.writestr(file_path, content)
        # Add empty directories
"""
    
    # Add empty directories
    for empty_dir in empty_dirs:
        script_content += f'        zipf.writestr("{empty_dir}/", "")\n'

    script_content += """
if __name__ == "__main__":
    create_zip()
    print("Zip file '{zip_name}' created successfully.")
"""

    # Write the generated script to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"Generated {output_file} successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a create_zip.py script from a directory")
    parser.add_argument("input_dir", help="Path to the input directory")
    parser.add_argument("--output", default="create_zip.py", help="Output file name (default: create_zip.py)")
    parser.add_argument("--zip-name", default="output.zip", help="Name of the zip file to create (default: output.zip)")
    args = parser.parse_args()

    generate_create_zip_script(args.input_dir, args.output, args.zip_name)
