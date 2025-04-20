import json

def generate_prompt(mapping, pyspark_code, output_dir):
    # Step 1: Generate prompt text
    prompt = f"Mapping: {mapping['mapping_name']} in folder {mapping['folder']}\n"
    
    prompt += "Sources:\n"
    for src in mapping['sources']:
        prompt += f"- {src['name']} ({src['type']})\n"

    prompt += "Targets:\n"
    for tgt in mapping['targets']:
        prompt += f"- {tgt['name']} ({tgt['type']})\n"

    prompt += "Connectors:\n"
    for conn in mapping['connectors']:
        prompt += f"- {conn['from_instance']}.{conn['from_field']} → {conn['to_instance']}.{conn['to_field']}\n"

    prompt += "Transformations:\n"
    for tf in mapping['transformations']:
        prompt += f"- {tf['name']} ({tf['type']})\n"
        if tf['sql_override']:
            prompt += f"  SQL Override: {tf['sql_override']}\n"
        if tf['filter_condition']:
            prompt += f"  Filter: {tf['filter_condition']}\n"

    # Step 2: Define JSONL file name
    filename = f"{mapping['mapping_name']}.jsonl"
    file_path = os.path.join(output_dir, filename)

    # Step 3: Save to JSONL
    record = {
        "prompt": prompt,
        "completion": pyspark_code
    }
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record) + "\n")

    # Step 4: Return path
    return file_path
