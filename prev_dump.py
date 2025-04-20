# main

import os
from parser import parse_informatica_xml
from summarizer import summarize_mapping

def process_files(input_folder, output_folder):
    for file in os.listdir(input_folder):
        if file.endswith(".xml") or file.endswith(".txt"):
            filepath = os.path.join(input_folder, file)
            print(f"Processing {filepath}...")
            mappings = parse_informatica_xml(filepath)

            for mapping in mappings:
                summary = summarize_mapping(mapping)
                out_file = os.path.join(output_folder, f"{mapping['mapping_name']}.md")
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(summary)
                print(f"✅ Summary saved to {out_file}")

if __name__ == "__main__":
    process_files("inforamtica_xml", "output")

parser.py
from lxml import etree

def parse_informatica_xml(file_path):
    tree = etree.parse(file_path)
    root = tree.getroot()
    
    # Extract folders/mappings
    mappings = []
    for folder in root.xpath("//FOLDER"):
        folder_name = folder.attrib['NAME']
        for mapping in folder.xpath(".//MAPPING"):
            mappings.append({
                "folder": folder_name,
                "mapping_name": mapping.attrib['NAME'],
                "description": mapping.attrib.get('DESCRIPTION', ''),
                "sources": extract_sources(folder),
                "targets": extract_targets(folder),
                "transformations": extract_transformations(mapping),
            })
    return mappings
def extract_lookup_sql(transformation):
    for attr in transformation.xpath(".//TABLEATTRIBUTE"):
        if "Lookup Sql Override" in attr.attrib.get("NAME", ""):
            return attr.attrib.get("VALUE", "").replace("&#xD; &#xA;", "\n")
    return None

def extract_router_groups(transformation):
    groups = []
    for group in transformation.xpath(".//GROUP"):
        groups.append({
            "name": group.attrib.get("NAME"),
            "type": group.attrib.get("TYPE"),
            "expression": group.attrib.get("EXPRESSION", "")
        })
    return groups
def extract_expression_ports(transformation):
    fields = []
    for field in transformation.xpath(".//TRANSFORMFIELD"):
        fields.append({
            "name": field.attrib.get("NAME"),
            "datatype": field.attrib.get("DATATYPE"),
            "porttype": field.attrib.get("PORTTYPE"),
            "expression": field.attrib.get("EXPRESSION", ""),
        })
    return fields


def extract_sources(folder):
    return [
        {
            "name": src.attrib["NAME"],
            "type": src.attrib.get("DATABASETYPE", ""),
            "fields": [
                {
                    "name": fld.attrib["NAME"],
                    "datatype": fld.attrib["DATATYPE"],
                    "precision": fld.attrib.get("PRECISION", ""),
                    "scale": fld.attrib.get("SCALE", "")
                }
                for fld in src.xpath(".//SOURCEFIELD")
            ]
        }
        for src in folder.xpath(".//SOURCE")
    ]


def extract_targets(folder):
    return [
        {
            "name": tgt.attrib["NAME"],
            "type": tgt.attrib.get("DATABASETYPE", ""),
            "fields": [
                {
                    "name": fld.attrib["NAME"],
                    "datatype": fld.attrib["DATATYPE"],
                    "precision": fld.attrib.get("PRECISION", ""),
                    "scale": fld.attrib.get("SCALE", "")
                }
                for fld in tgt.xpath(".//TARGETFIELD")
            ]
        }
        for tgt in folder.xpath(".//TARGET")
    ]


def extract_transformations(mapping):
    return [
        {
            "name": tf.attrib["NAME"],
            "type": tf.attrib["TYPE"],
            "description": tf.attrib.get("DESCRIPTION", ""),
            "fields": [
                {
                    "name": field.attrib["NAME"],
                    "datatype": field.attrib["DATATYPE"],
                    "porttype": field.attrib["PORTTYPE"],
                    "expression": field.attrib.get("EXPRESSION", "")
                }
                for field in tf.xpath(".//TRANSFORMFIELD")
            ]
        }
        for tf in mapping.xpath(".//TRANSFORMATION")
    ]
def extract_connectors(mapping):
    return [{
        "from_field": conn.attrib.get("FROMFIELD"),
        "from_instance": conn.attrib.get("FROMINSTANCE"),
        "to_field": conn.attrib.get("TOFIELD"),
        "to_instance": conn.attrib.get("TOINSTANCE"),
    } for conn in mapping.xpath(".//CONNECTOR")]











ver--1

# main.py
import os
from lxml import etree
from parser import parse_informatica_xml
from utils import clean_broken_xml

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
        lines.append(f"### {tf['name']} ({tf['type']})")
        if tf['sql_override']:
            lines.append("**Lookup SQL Override:**")
            lines.append(f"```sql\n{tf['sql_override']}\n```")
        for f in tf['fields']:
            lines.append(f"- `{f['name']}`: {f['datatype']} | {f['porttype']} | {f['expression']}")

    return "\n".join(lines)

def process_files(input_folder, output_folder):
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
            except Exception as e:
                print(f"❌ Failed to parse {file}: {e}")

if __name__ == "__main__":
    process_files("inforamtica_xml", "output")

--parser.py

# parser.py
from lxml import etree

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
            })
    return mappings

def extract_sources(folder):
    sources = []
    for src_def in folder.xpath(".//SOURCE"):
        fields = []
        for f in src_def.xpath(".//SOURCEFIELD"):
            fields.append({
                "name": f.attrib.get("NAME"),
                "datatype": f.attrib.get("DATATYPE"),
                "precision": f.attrib.get("PRECISION", ""),
                "scale": f.attrib.get("SCALE", "")
            })
        sources.append({
            "name": src_def.attrib.get("NAME"),
            "type": src_def.attrib.get("DATABASETYPE", ""),
            "fields": fields
        })
    return sources

def extract_targets(folder):
    targets = []
    for tgt_def in folder.xpath(".//TARGET"):
        fields = []
        for f in tgt_def.xpath(".//TARGETFIELD"):
            fields.append({
                "name": f.attrib.get("NAME"),
                "datatype": f.attrib.get("DATATYPE"),
                "precision": f.attrib.get("PRECISION", ""),
                "scale": f.attrib.get("SCALE", "")
            })
        targets.append({
            "name": tgt_def.attrib.get("NAME"),
            "type": tgt_def.attrib.get("DATABASETYPE", ""),
            "fields": fields
        })
    return targets

def extract_transformations(mapping):
    transformations = []
    for tf in mapping.xpath(".//TRANSFORMATION"):
        sql_override = None
        for attr in tf.xpath(".//TABLEATTRIBUTE"):
            if "Lookup Sql Override" in attr.attrib.get("NAME", ""):
                sql_override = attr.attrib.get("VALUE", "").replace("&#xD; &#xA;", "\n")
        fields = [
            {
                "name": f.attrib.get("NAME"),
                "datatype": f.attrib.get("DATATYPE"),
                "porttype": f.attrib.get("PORTTYPE"),
                "expression": f.attrib.get("EXPRESSION", ""),
                "expression_type": f.attrib.get("EXPRESSIONTYPE", "")
            }
            for f in tf.xpath(".//TRANSFORMFIELD")
        ]
        transformations.append({
            "name": tf.attrib.get("NAME"),
            "type": tf.attrib.get("TYPE"),
            "description": tf.attrib.get("DESCRIPTION", ""),
            "fields": fields,
            "sql_override": sql_override,
        })
    return transformations






##parse.py code now

# parser.py
from lxml import etree

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

    # Also include SHORTCUTs that reference SOURCE
    for shortcut in folder.xpath(".//SHORTCUT[@OBJECTTYPE='SOURCE']"):
        sources.append({
            "name": shortcut.attrib.get("NAME"),
            "type": shortcut.attrib.get("DBDNAME", shortcut.attrib.get("REFOBJECTNAME")),
            "fields": []  # no fields in shortcut definition
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

    # Also include SHORTCUTs that reference TARGET
    for shortcut in folder.xpath(".//SHORTCUT[@OBJECTTYPE='TARGET']"):
        targets.append({
            "name": shortcut.attrib.get("NAME"),
            "type": shortcut.attrib.get("REFOBJECTNAME"),
            "fields": []  # no field metadata here either
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

        # Step 1: Extract router groups (if any)
        groups = []
        for g in tf.xpath(".//GROUP"):
            groups.append({
                "name": g.attrib.get("NAME"),
                "type": g.attrib.get("TYPE"),
                "expression": g.attrib.get("EXPRESSION", ""),
                "order": g.attrib.get("ORDER", "")
            })

        # Step 2: Extract transform fields and assign to group
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
