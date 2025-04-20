from lxml import etree
import json
import sys
import os

# ---- Parsing Informatica XML ---- #

def parse_informatica_xml(tree):
    root = tree
    mappings = []
    for folder in root.xpath("//FOLDER"):
        folder_name = folder.attrib.get('NAME')
        for mapping in folder.xpath(".//MAPPING"):
            mappings.append({
                "folder": folder_name,
                "mapping_name": mapping.attrib.get('NAME'),
                "description": mapping.attrib.get('DESCRIPTION', ''),
                "sources": extract_sources(folder),
                "targets": extract_targets(folder),
                "transformations": extract_transformations(mapping),
                "connectors": extract_connectors(mapping)
            })
    return mappings

def extract_sources(folder):
    sources = []
    for src in folder.xpath(".//SOURCE"):
        fields = []
        for f in src.xpath(".//SOURCEFIELD"):
            fields.append({
                "name": f.attrib.get("NAME"),
                "datatype": f.attrib.get("DATATYPE"),
                "precision": f.attrib.get("PRECISION", ""),
                "scale": f.attrib.get("SCALE", "")
            })
        sources.append({
            "name": src.attrib.get("NAME"),
            "type": src.attrib.get("DATABASETYPE", ""),
            "fields": fields
        })
    for shortcut in folder.xpath(".//SHORTCUT[@OBJECTTYPE='SOURCE']"):
        sources.append({
            "name": shortcut.attrib.get("NAME"),
            "type": shortcut.attrib.get("DBDNAME", shortcut.attrib.get("REFOBJECTNAME")),
            "fields": []
        })
    return sources

def extract_targets(folder):
    targets = []
    for tgt in folder.xpath(".//TARGET"):
        fields = []
        for f in tgt.xpath(".//TARGETFIELD"):
            fields.append({
                "name": f.attrib.get("NAME"),
                "datatype": f.attrib.get("DATATYPE"),
                "precision": f.attrib.get("PRECISION", ""),
                "scale": f.attrib.get("SCALE", "")
            })
        targets.append({
            "name": tgt.attrib.get("NAME"),
            "type": tgt.attrib.get("DATABASETYPE", ""),
            "fields": fields
        })
    for shortcut in folder.xpath(".//SHORTCUT[@OBJECTTYPE='TARGET']"):
        targets.append({
            "name": shortcut.attrib.get("NAME"),
            "type": shortcut.attrib.get("REFOBJECTNAME"),
            "fields": []
        })
    return targets

def extract_transformations(mapping):
    transformations = []
    for tf in mapping.xpath(".//TRANSFORMATION"):
        sql_override = None
        filter_condition = None
        for attr in tf.xpath(".//TABLEATTRIBUTE"):
            name = attr.attrib.get("NAME", "")
            if name == "Lookup Sql Override":
                sql_override = attr.attrib.get("VALUE", "").replace("&#xD; &#xA;", "\n")
            elif name == "Filter Condition":
                filter_condition = attr.attrib.get("VALUE", "").replace("&#xD; &#xA;", "\n")
        groups = []
        for g in tf.xpath(".//GROUP"):
            groups.append({
                "name": g.attrib.get("NAME"),
                "type": g.attrib.get("TYPE"),
                "expression": g.attrib.get("EXPRESSION", ""),
                "order": g.attrib.get("ORDER", "")
            })
        fields_by_group = {}
        for f in tf.xpath(".//TRANSFORMFIELD"):
            group = f.attrib.get("GROUP", "default")
            field = {
                "name": f.attrib.get("NAME"),
                "datatype": f.attrib.get("DATATYPE"),
                "porttype": f.attrib.get("PORTTYPE"),
                "defaultvalue": f.attrib.get("DEFAULTVALUE", ""),
                "expression": f.attrib.get("EXPRESSION", ""),
                "expression_type": f.attrib.get("EXPRESSIONTYPE", ""),
                "picturetext": f.attrib.get("PICTURETEXT", ""),
                "precision": f.attrib.get("PRECISION", ""),
                "scale": f.attrib.get("SCALE", "")
            }
            fields_by_group.setdefault(group, []).append(field)
        transformations.append({
            "name": tf.attrib.get("NAME"),
            "type": tf.attrib.get("TYPE"),
            "description": tf.attrib.get("DESCRIPTION", ""),
            "groups": groups,
            "fields_by_group": fields_by_group,
            "sql_override": sql_override,
            "filter_condition": filter_condition,
        })
    return transformations

def extract_connectors(mapping):
    connectors = []
    for conn in mapping.xpath(".//CONNECTOR"):
        connectors.append({
            "from_instance": conn.attrib.get("FROMINSTANCE"),
            "from_field": conn.attrib.get("FROMFIELD"),
            "to_instance": conn.attrib.get("TOINSTANCE"),
            "to_field": conn.attrib.get("TOFIELD"),
            "from_type": conn.attrib.get("FROMINSTANCETYPE"),
            "to_type": conn.attrib.get("TOINSTANCETYPE"),
        })
    return connectors

# ---- Prompt Generator ---- #

def generate_prompt(mapping):
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
    return prompt

# ---- JSONL Writer ---- #

def save_to_jsonl(mapping_prompt, pyspark_code, file_path):
    record = {
        "prompt": mapping_prompt,
        "completion": pyspark_code
    }
    with open(file_path, 'a') as f:
        f.write(json.dumps(record) + "\n")

# ---- CLI Entrypoint ---- #

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python parser.py <mapping.xml> <output.jsonl>")
        sys.exit(1)

    xml_file = sys.argv[1]
    output_jsonl = sys.argv[2]

    tree = etree.parse(xml_file)
    mappings = parse_informatica_xml(tree)

    for mapping in mappings:
        prompt = generate_prompt(mapping)

        # Manual step for now:
        print("\n--- Prompt ---\n")
        print(prompt)
        print("\nAdd the corresponding PySpark code for this mapping into the script.\n")

        pyspark_code = "# TODO: Write equivalent PySpark code for this mapping"

        save_to_jsonl(prompt, pyspark_code, output_jsonl)

    print(f"Processed {len(mappings)} mappings into {output_jsonl}")
