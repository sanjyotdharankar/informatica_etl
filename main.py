# main.py
import os
from lxml import etree
from parser import *
from utils import clean_broken_xml
from etl_graph_networkx import generate_etl_diagram
# from code_generator import generate_etl_script
# from pandas_generator import generate_pandas_code

# from xml_jsonl_file import xml_to_jsonl
# from graph import generate_etl_graph
# from diagrams_graph import generate_etl_diagram
# from promt import generate_prompt
from jsonl_converter import convert_md_py_to_jsonl
from parse_md import combine_md_py_to_jsonl_flexible
from training.fine_tune_llama import fine_tune_model

def summarize_mapping(mapping):
    lines = [f"# Mapping: {mapping['mapping_name']}",
             f"**Folder:** {mapping['folder']}",
             f"**Description:** {mapping.get('description', '')}\n"]

    lines.append("\n## 📂 Source Definitions")
    for src in mapping['sources']:
        lines.append(f"### {src['name']} ({src['type']})")
        for f in src['fields']:
            lines.append(f"- `{f['name']}`: {f['datatype']} ({f['precision']},{f['scale']})")

    lines.append("\n## 🎯 Target Definitions")
    for tgt in mapping['targets']:
        lines.append(f"### {tgt['name']} ({tgt['type']})")
        for f in tgt['fields']:
            lines.append(f"- `{f['name']}`: {f['datatype']} ({f['precision']},{f['scale']})")

    lines.append("\n## 🔄 Transformations")
    for tf in mapping['transformations']:
        lines.append(f"\n### {tf['name']} ({tf['type']})")
        if tf['sql_override']:
            lines.append("**SQL Override:**")
            lines.append(f"```sql\n{tf['sql_override']}\n```")
        if tf['filter_condition']:
            lines.append("**Filter Condition:**")
            lines.append(f"```text\n{tf['filter_condition']}\n```")

        # Router/Expression/etc. groups
        if tf.get('groups'):
            lines.append("**Groups:**")
            for g in tf['groups']:
                g_expr = g['expression'].replace("\n", " ") if g['expression'] else "(no condition)"
                lines.append(f"- `{g['name']}` ({g['type']}): `{g_expr}`")

        # Grouped Fields
        lines.append("**Fields by Group:**")
        for group_name, fields in tf['fields_by_group'].items():
            lines.append(f"\n#### Group: {group_name}")
            for f in fields:
                logic = f['expression'] or f['defaultvalue'] or "No logic"
                lines.append(
                    f"- `{f['name']}` ({f['datatype']}, {f['porttype']}) → {logic} "
                    f"(Precision: {f['precision']}, Scale: {f['scale']})"
                )


    lines.append("\n## 🔁 Connector Flow")
    for conn in mapping['connectors']:
        lines.append(
            f"- `{conn['from_instance']}`.`{conn['from_field']}` "
            f"➝ `{conn['to_instance']}`.`{conn['to_field']}`"
        )

    return "\n".join(lines)

def process_files(input_folder, output_folder,training):
    for file in os.listdir(input_folder):
        if file.endswith(".xml") or file.endswith(".txt"):
            filepath = os.path.join(input_folder, file)
            print(f"Processing {filepath}...")
            with open(filepath, 'r', encoding='utf-8') as f:
                raw_text = f.read()
            clean_text = clean_broken_xml(raw_text)
            try:
                tree = etree.fromstring(clean_text.encode('utf-8'))
                mappings = parse_informatica_xml(tree)
                for mapping in mappings:
                    summary = summarize_mapping(mapping)
                    out_file = os.path.join(output_folder, f"{mapping['mapping_name']}.md")
                    with open(out_file, "w", encoding='utf-8') as f:
                        f.write(summary)
                    print(f"✅ Summary saved to {out_file}")
                img_path = generate_etl_diagram(mapping, output_folder)
                print(f"🖼️ ETL image saved to {img_path}")
                #convert in jsonl
                convert_md_py_to_jsonl(output_folder, training)
                # print(f"📈 Training data saved to {output_folder}/training_data.jsonl")
                # 🔄 Example usage
                combine_md_py_to_jsonl_flexible(output_folder, "train_advanced.jsonl")
                #run the fine_tune_llama.py
                # Call the function to fine-tune the model
                fine_tune_model()
            except Exception as e:
                print(f"❌ Failed to parse {file}: {e}")

if __name__ == "__main__":
    process_files("inforamtica_xml", "output","output/training")
