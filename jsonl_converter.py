import os
import json

def convert_md_py_to_jsonl(input_folder, output_folder):
    """
    Converts .md and .py files into individual .jsonl files based on mapping names.
    
    Args:
        input_folder (str): Folder with .md and .py files.
        output_folder (str): Folder to write .jsonl files to.
    """
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        if file.endswith('.md'):
            base_name = os.path.splitext(file)[0]
            md_path = os.path.join(input_folder, f"{base_name}.md")
            py_path = os.path.join(input_folder, f"{base_name}.py")

            if os.path.exists(py_path):
                with open(md_path, 'r', encoding='utf-8') as md_file:
                    prompt = md_file.read().strip()

                with open(py_path, 'r', encoding='utf-8') as py_file:
                    completion = py_file.read().strip()

                entry = {
                    "prompt": prompt,
                    "completion": f"\n```python\n{completion}\n```"
                }

                # ✅ Generate output file per mapping
                out_file_jsonl = os.path.join(output_folder, f"{base_name}.jsonl")
                with open(out_file_jsonl, 'w', encoding='utf-8') as out_file:
                    json.dump(entry, out_file)
                    out_file.write('\n')

                print(f"✅ Created: {out_file_jsonl}")
            else:
                print(f"⚠️ Skipped: No .py for {base_name}")
