import os
import re
import json

def extract_section_table(content, section_title):
    pattern = rf"### ([A-Z0-9_]+).*?\(.*?\)"
    matches = re.findall(pattern, content)
    if section_title.lower() == "source":
        return matches[0] if len(matches) >= 1 else "UnknownSource"
    elif section_title.lower() == "target":
        return matches[1] if len(matches) >= 2 else "UnknownTarget"
    return "Unknown"

def extract_field_details(content, section_title):
    # Find field names and types
    pattern = r"- `([^`]+)`:\s*(\w+)\s*\(([\d,]+)\)"
    matches = re.findall(pattern, content)
    fields = {}
    for field, field_type, precision_scale in matches:
        fields[field] = {
            "type": field_type,
            "precision_scale": precision_scale
        }
    return fields

def extract_connector_flows(content):
    flows = re.findall(r"- `(.*?)`\s*[➝→]\s*`(.*?)`", content)
    return [f"{src} -> {dst}" for src, dst in flows]

def extract_sql_blocks(content):
    return re.findall(r"```sql\n(.*?)```", content, re.DOTALL | re.IGNORECASE)

def extract_expressions(content):
    return re.findall(r"→\s*(IIF\(.*?\))", content)

def extract_mapping_name(content):
    match = re.search(r"# Mapping:\s*(.*)", content)
    return match.group(1).strip() if match else "UnknownMapping"

def parse_md_flexibly(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    mapping_name = extract_mapping_name(content)
    source_table = extract_section_table(content, "source")
    target_table = extract_section_table(content, "target")
    flows = extract_connector_flows(content)
    sql_blocks = extract_sql_blocks(content)
    expressions = extract_expressions(content)

    # Parse source and target fields (including types, precision, and scale)
    source_fields = extract_field_details(content, "source")
    target_fields = extract_field_details(content, "target")

    # Building the prompt
    prompt_lines = [
        f"Mapping: {mapping_name}",
        f"Source: {source_table}",
        f"Target: {target_table}",
        "Source Fields:"
    ]
    
    for field, details in source_fields.items():
        prompt_lines.append(f"- `{field}`: {details['type']} ({details['precision_scale']})")

    prompt_lines.append("Target Fields:")
    for field, details in target_fields.items():
        prompt_lines.append(f"- `{field}`: {details['type']} ({details['precision_scale']})")

    prompt_lines.append("Transformations:")
    for sql in sql_blocks:
        prompt_lines.append(f"- SQL: {sql.strip()}")
    for expr in expressions:
        prompt_lines.append(f"- Expression: {expr.strip()}")

    if flows:
        prompt_lines.append("Connector Flow:")
        prompt_lines += [f"- {f}" for f in flows]

    return "\n".join(prompt_lines)

def combine_md_py_to_jsonl_flexible(input_folder, output_jsonl_file):
    entries = []
    for file in os.listdir(input_folder):
        if file.endswith(".md"):
            base_name = os.path.splitext(file)[0]
            md_path = os.path.join(input_folder, file)
            py_path = os.path.join(input_folder, f"{base_name}.py") 

            if os.path.exists(py_path):
                prompt = parse_md_flexibly(md_path)
                with open(py_path, 'r', encoding='utf-8') as f:
                    completion = f.read().strip()
                entry = {
                    "prompt": prompt,
                    "completion": f"\n```python\n{completion}\n```"
                }
                entries.append(entry)
                print(f"✅ Processed: {base_name}")
            else:
                print(f"⚠️ Skipped: Missing _pyspark.py for {base_name}")

    with open(output_jsonl_file, 'w', encoding='utf-8') as out_file:
        for entry in entries:
            json.dump(entry, out_file)
            out_file.write('\n')

    print(f"\n✅ All entries saved to: {output_jsonl_file}")


