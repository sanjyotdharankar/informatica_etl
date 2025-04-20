import xml.etree.ElementTree as ET
import json
import os

def xml_to_jsonl(xml_folder, jsonl_output):
    with open(jsonl_output, "w") as out_file:
        for filename in os.listdir(xml_folder):
            print(f"Processing {filename}...")
            if filename.endswith(".xml"):
                tree = ET.parse(os.path.join(xml_folder, filename))
                root = tree.getroot()

                # You’ll need to modify this based on XML structure
                for element in root.findall(".//record"):  # adjust tag
                    instruction = element.find("question").text
                    output = element.find("answer").text

                    record = {
                        "instruction": instruction,
                        "input": "",
                        "output": output
                    }
                    out_file.write(json.dumps(record) + "\n")


