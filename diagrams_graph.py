# diagrams_graph.py
from diagrams import Diagram, Edge
from diagrams.custom import Custom
import os

def generate_etl_diagram(mapping, output_folder):
    diagram_name = mapping['mapping_name'] + "_etl"
    output_path = os.path.join(output_folder, diagram_name)

    with Diagram(f"ETL Flow: {mapping['mapping_name']}", filename=output_path, outformat="png", show=False):
        node_map = {}

        # Fallback icons (you can replace these with real image paths later)
        def icon(label):
            return Custom(label, "./icons/default.png")

        # Source nodes
        for src in mapping['sources']:
            label = f"{src['name']}\n(SOURCE)"
            node_map[src['name']] = icon(label)

        # Target nodes
        for tgt in mapping['targets']:
            label = f"{tgt['name']}\n(TARGET)"
            node_map[tgt['name']] = icon(label)

        # Transformation nodes
        for tf in mapping['transformations']:
            label = f"{tf['name']}\n({tf['type']})"
            node_map[tf['name']] = icon(label)

        # Connectors
        for conn in mapping.get("connectors", []):
            src_node = node_map.get(conn["from_instance"])
            tgt_node = node_map.get(conn["to_instance"])
            if src_node and tgt_node:
                src_node >> Edge(label=f"{conn['from_field']} → {conn['to_field']}") >> tgt_node

    return output_path + ".png"
