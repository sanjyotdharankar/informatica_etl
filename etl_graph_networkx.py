# # # etl_graph_networkx.py
# # import matplotlib.pyplot as plt
# # import networkx as nx
# # import os

# # def generate_etl_diagram(mapping, output_folder):
# #     G = nx.DiGraph()

# #     # Use only FROMINSTANCE → TOINSTANCE pairs (skip columns)
# #     for conn in mapping.get("connectors", []):
# #         src = conn["from_instance"]
# #         tgt = conn["to_instance"]
# #         G.add_edge(src, tgt)

# #     pos = nx.spring_layout(G, k=0.6, iterations=50)

# #     # Style
# #     plt.figure(figsize=(12, 8))
# #     nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", arrowsize=20)

# #     # Save image
# #     output_path = os.path.join(output_folder, f"{mapping['mapping_name']}_etl.png")
# #     plt.title(f"ETL Flow: {mapping['mapping_name']}", fontsize=14)
# #     plt.savefig(output_path, format="png")
# #     plt.close()

# #     return output_path
# # # --ver2
# # # import matplotlib.pyplot as plt
# # # import networkx as nx
# # # import os

# # # def generate_etl_diagram(mapping, output_folder):
# # #     G = nx.DiGraph()

# # #     # Step 1: Build a node-type map (source / target / transformation)
# # #     node_roles = {}

# # #     for src in mapping.get("sources", []):
# # #         node_roles[src["name"]] = "source"
# # #     for tgt in mapping.get("targets", []):
# # #         node_roles[tgt["name"]] = "target"
# # #     for tf in mapping.get("transformations", []):
# # #         node_roles[tf["name"]] = "transformation"

# # #     # Step 2: Add edges
# # #     for conn in mapping.get("connectors", []):
# # #         src = conn["from_instance"]
# # #         tgt = conn["to_instance"]
# # #         G.add_edge(src, tgt)
# # #         node_roles.setdefault(src, "unknown")
# # #         node_roles.setdefault(tgt, "unknown")

# # #     # Step 3: Layout
# # #     try:
# # #         from networkx.drawing.nx_agraph import graphviz_layout
# # #         pos = graphviz_layout(G, prog="dot")
# # #     except:
# # #         pos = nx.spring_layout(G, k=1, iterations=100)

# # #     # Step 4: Color by type
# # #     color_map = {
# # #         "source": "lightskyblue",
# # #         "target": "lightgreen",
# # #         "transformation": "lightyellow",
# # #         "unknown": "gray"
# # #     }
# # #     node_colors = [color_map.get(node_roles.get(node, "unknown"), "gray") for node in G.nodes]

# # #     # Step 5: Draw graph
# # #     plt.figure(figsize=(14, 8))
# # #     plt.title(f"ETL Workflow: {mapping['mapping_name']}", fontsize=16, weight='bold')

# # #     nx.draw(
# # #         G,
# # #         pos,
# # #         with_labels=True,
# # #         node_color=node_colors,
# # #         node_size=3000,
# # #         font_size=10,
# # #         font_weight="bold",
# # #         edge_color='gray',
# # #         arrows=True,
# # #         arrowsize=20
# # #     )

# # #     output_path = os.path.join(output_folder, f"{mapping['mapping_name']}_etl.png")
# # #     plt.tight_layout()
# # #     plt.savefig(output_path, format="png", dpi=300)
# # #     plt.close()

# # #     return output_path


# # # --ver3    
# # # etl_graph_networkx.py

# # # import matplotlib.pyplot as plt
# # # import networkx as nx
# # # import os

# # # def generate_etl_diagram(mapping, output_folder):
# # #     G = nx.DiGraph()

# # #     # Step 1: Build a node-type map (source / target / transformation)
# # #     node_roles = {}

# # #     for src in mapping.get("sources", []):
# # #         node_roles[src["name"]] = "source"
# # #     for tgt in mapping.get("targets", []):
# # #         node_roles[tgt["name"]] = "target"
# # #     for tf in mapping.get("transformations", []):
# # #         node_roles[tf["name"]] = "transformation"

# # #     # Step 2: Add edges
# # #     for conn in mapping.get("connectors", []):
# # #         src = conn["from_instance"]
# # #         tgt = conn["to_instance"]
# # #         G.add_edge(src, tgt)
# # #         node_roles.setdefault(src, "unknown")
# # #         node_roles.setdefault(tgt, "unknown")

# # #     # Step 3: Layout with padding
# # #     pos = nx.spring_layout(G, k=1.5, iterations=200)  # k controls spacing between nodes

# # #     # Step 4: Color nodes by type
# # #     color_map = {
# # #         "source": "lightskyblue",
# # #         "target": "lightgreen",
# # #         "transformation": "lightyellow",
# # #         "unknown": "gray"
# # #     }
# # #     node_colors = [color_map.get(node_roles.get(node, "unknown"), "gray") for node in G.nodes]

# # #     # Step 5: Draw graph
# # #     plt.figure(figsize=(16, 10))
# # #     plt.title(f"ETL Workflow: {mapping['mapping_name']}", fontsize=16, weight='bold', pad=20)

# # #     nx.draw_networkx_nodes(
# # #         G, pos,
# # #         node_color=node_colors,
# # #         node_size=3500,
# # #         linewidths=2,
# # #         edgecolors="black"
# # #     )
# # #     nx.draw_networkx_edges(
# # #         G, pos,
# # #         arrowstyle="-|>",
# # #         arrowsize=20,
# # #         edge_color="gray",
# # #         width=2
# # #     )
# # #     nx.draw_networkx_labels(
# # #         G, pos,
# # #         font_size=10,
# # #         font_weight="bold",
# # #         font_color="black",
# # #         verticalalignment='center',
# # #         horizontalalignment='center'
# # #     )

# # #     plt.axis('off')
# # #     plt.tight_layout(pad=3.0)

# # #     # Step 6: Save image
# # #     output_path = os.path.join(output_folder, f"{mapping['mapping_name']}_etl.png")
# # #     plt.savefig(output_path, format="png", dpi=300)
# # #     plt.close()

# # #     return output_path

# # # --ver3

# # import matplotlib.pyplot as plt
# # import networkx as nx
# # from matplotlib.patches import FancyArrowPatch
# # from matplotlib import collections as mc
# # import os


# # def generate_etl_diagram(mapping, output_folder):
# #     G = nx.DiGraph()
# #     node_roles = {}

# #     # Step 1: Classify nodes
# #     for src in mapping.get("sources", []):
# #         node_roles[src["name"]] = "source"
# #     for tgt in mapping.get("targets", []):
# #         node_roles[tgt["name"]] = "target"
# #     for tf in mapping.get("transformations", []):
# #         ttype = tf["type"].lower()
# #         if "router" in ttype:
# #             role = "router"
# #         elif "expression" in ttype:
# #             role = "expression"
# #         elif "qualifier" in ttype:
# #             role = "source_qualifier"
# #         else:
# #             role = "transformation"
# #         node_roles[tf["name"]] = role

# #     # Step 2: Add connectors
# #     for conn in mapping.get("connectors", []):
# #         src = conn["from_instance"]
# #         tgt = conn["to_instance"]
# #         G.add_edge(src, tgt)
# #         node_roles.setdefault(src, "unknown")
# #         node_roles.setdefault(tgt, "unknown")

# #     # Step 3: Manual layout (left to right)
# #     role_order = {
# #         "source": 0,
# #         "source_qualifier": 1,
# #         "expression": 2,
# #         "router": 3,
# #         "transformation": 2.5,
# #         "target": 4,
# #         "unknown": 5,
# #     }

# #     layers = {}
# #     pos = {}

# #     for node in G.nodes:
# #         role = node_roles.get(node, "unknown")
# #         x = role_order.get(role, 5)
# #         layers.setdefault(x, []).append(node)

# #     # Arrange vertically with spacing
# #     for x, nodes in layers.items():
# #         for i, node in enumerate(nodes):
# #             y = -i * 2
# #             pos[node] = (x * 4, y)  # Horizontal spacing

# #     # Step 4: Color coding
# #     color_map = {
# #         "source": "lightskyblue",
# #         "source_qualifier": "deepskyblue",
# #         "expression": "lightyellow",
# #         "router": "orange",
# #         "transformation": "khaki",
# #         "target": "lightgreen",
# #         "unknown": "lightgray"
# #     }

# #     node_colors = [
# #         color_map.get(node_roles.get(n, "unknown"), "lightgray")
# #         for n in G.nodes
# #     ]

# #     # Step 5: Plotting
# #     plt.figure(figsize=(18, 10))
# #     plt.title(f"ETL Workflow: {mapping['mapping_name']}", fontsize=16, weight='bold', pad=20)

# #     nx.draw_networkx_nodes(
# #         G, pos,
# #         node_color=node_colors,
# #         node_size=4000,
# #         edgecolors='black',
# #         linewidths=1.5
# #     )
# #     nx.draw_networkx_labels(
# #         G, pos,
# #         font_size=9,
# #         font_weight='bold',
# #         font_color='black'
# #     )

# #     # Step 6: Draw explicit arrows with FancyArrowPatch
# #     ax = plt.gca()
# #     for src, tgt in G.edges():
# #         x1, y1 = pos[src]
# #         x2, y2 = pos[tgt]
# #         arrow = FancyArrowPatch(
# #             (x1, y1), (x2, y2),
# #             arrowstyle='-|>',
# #             mutation_scale=20,
# #             linewidth=2,
# #             color='gray',
# #             connectionstyle="arc3,rad=0.05"
# #         )
# #         ax.add_patch(arrow)

# #     plt.axis("off")
# #     plt.tight_layout(pad=2.0)

# #     output_path = os.path.join(output_folder, f"{mapping['mapping_name']}_etl.png")
# #     plt.savefig(output_path, format="png", dpi=300)
# #     plt.close()

# #     return output_path

# # # --ver4  great

# # import os
# # import matplotlib.pyplot as plt
# # import networkx as nx

# # def generate_etl_diagram(mapping, output_folder):
# #     G = nx.DiGraph()

# #     # Create node labels
# #     for src in mapping['sources']:
# #         G.add_node(src['name'], type='source')

# #     for tf in mapping['transformations']:
# #         G.add_node(tf['name'], type='transformation')

# #     for tgt in mapping['targets']:
# #         G.add_node(tgt['name'], type='target')

# #     # Add edges using connectors
# #     for conn in mapping['connectors']:
# #         from_node = conn['from_instance']
# #         to_node = conn['to_instance']
# #         G.add_edge(from_node, to_node)

# #     # Layout (avoid overlaps)
# #     pos = nx.spring_layout(G, k=1.5, iterations=200)

# #     # Draw nodes
# #     node_colors = []
# #     for node in G.nodes(data=True):
# #         if node[1]['type'] == 'source':
# #             node_colors.append('skyblue')
# #         elif node[1]['type'] == 'target':
# #             node_colors.append('lightgreen')
# #         else:
# #             node_colors.append('lightgray')

# #     plt.figure(figsize=(14, 10))
# #     nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors,
# #             font_size=10, font_weight='bold', arrows=True, arrowstyle='-|>', edge_color='black')

# #     # Save as PNG
# #     filename = os.path.join(output_folder, f"{mapping['mapping_name']}_etl.png")
# #     plt.savefig(filename, bbox_inches='tight')
# #     plt.close()
# #     return filename

# # --ver5 

# # import os
# # import matplotlib.pyplot as plt
# # import networkx as nx

# # def generate_etl_diagram(mapping, output_folder):
# #     G = nx.DiGraph()

# #     sources = [s['name'] for s in mapping['sources']]
# #     targets = [t['name'] for t in mapping['targets']]
# #     transformations = [t['name'] for t in mapping['transformations']]

# #     connected_nodes = set()
# #     for conn in mapping['connectors']:
# #         from_node = conn['from_instance']
# #         to_node = conn['to_instance']
# #         if from_node and to_node:
# #             G.add_edge(from_node, to_node)
# #             connected_nodes.add(from_node)
# #             connected_nodes.add(to_node)

# #     for node in sources:
# #         G.add_node(node, type='source')
# #     for node in transformations:
# #         G.add_node(node, type='transformation')
# #     for node in targets:
# #         G.add_node(node, type='target')

# #     # Use spring layout for connected graph for clear flow
# #     connected_subgraph = G.subgraph(connected_nodes)
# #     pos_connected = nx.spring_layout(connected_subgraph, k=1.5, iterations=100)

# #     # Place disconnected nodes separately below the flow
# #     pos = dict(pos_connected)
# #     disconnected = [n for n in G.nodes if n not in connected_nodes]

# #     y_min = min([y for _, y in pos_connected.values()]) if pos_connected else 0
# #     y_disconnected = y_min - 2
# #     x_start = 0
# #     for i, node in enumerate(disconnected):
# #         pos[node] = (x_start + i * 5, y_disconnected)

# #     # Color map
# #     color_map = []
# #     for node in G:
# #         node_type = G.nodes[node].get('type')
# #         if node_type == 'source':
# #             color_map.append('skyblue')
# #         elif node_type == 'target':
# #             color_map.append('lightgreen')
# #         else:
# #             color_map.append('lightgray')

# #     plt.figure(figsize=(16, 10))
# #     nx.draw(
# #         G, pos,
# #         with_labels=True,
# #         node_color=color_map,
# #         node_size=3000,
# #         font_size=9,
# #         font_weight='bold',
# #         arrows=True,
# #         edge_color='gray',
# #         arrowstyle='-|>',
# #         linewidths=1
# #     )

# #     filename = os.path.join(output_folder, f"{mapping['mapping_name']}_diagram.png")
# #     plt.savefig(filename, bbox_inches='tight')
# #     plt.close()
# #     return filename


# # --ver6 great
# # import os
# # import matplotlib.pyplot as plt
# # import networkx as nx

# # def generate_etl_diagram(mapping, output_folder):
# #     G = nx.DiGraph()

# #     # Add nodes and label their types
# #     for src in mapping['sources']:
# #         G.add_node(src['name'], type='Source Definition')

# #     for tf in mapping['transformations']:
# #         G.add_node(tf['name'], type=tf['type'])

# #     for tgt in mapping['targets']:
# #         G.add_node(tgt['name'], type='Target Definition')

# #     for conn in mapping['connectors']:
# #         from_node = conn['from_instance']
# #         to_node = conn['to_instance']
# #         G.add_edge(from_node, to_node)

# #     # Define manual layer ordering
# #     layer_order = [
# #         "Lookup Procedure",
# #         "Source Definition",
# #         "Shortcut",
# #         "Application Source Qualifier",
# #         "Joiner",
# #         "Expression",
# #         "Filter",
# #         "Router",
# #         "Expression_to_Target",
# #         "Target Definition"
# #     ]

# #     # Assign positions
# #     pos = {}
# #     layer_y = {layer: -i * 2 for i, layer in enumerate(layer_order)}
# #     layer_x_tracker = {layer: 0 for layer in layer_order}

# #     for node, data in G.nodes(data=True):
# #         node_type = data.get('type', 'Expression')

# #         # Map shortcut source/target manually if needed
# #         if 'Shortcut' in node and 'Source' in node:
# #             node_type = 'Shortcut'
# #         elif 'Shortcut' in node and 'Target' in node:
# #             node_type = 'Shortcut'

# #         y = layer_y.get(node_type, -20)
# #         x = layer_x_tracker.get(node_type, 0)
# #         pos[node] = (x * 5, y)
# #         layer_x_tracker[node_type] = x + 1

# #     # Set node colors
# #     color_map = []
# #     for node in G:
# #         node_type = G.nodes[node].get('type')
# #         if node_type == 'Source Definition':
# #             color_map.append('skyblue')
# #         elif node_type == 'Target Definition':
# #             color_map.append('lightgreen')
# #         elif node_type == 'Lookup Procedure':
# #             color_map.append('plum')
# #         elif node_type == 'Application Source Qualifier':
# #             color_map.append('orange')
# #         elif node_type == 'Joiner':
# #             color_map.append('gold')
# #         elif node_type == 'Filter':
# #             color_map.append('red')
# #         elif node_type == 'Router':
# #             color_map.append('tomato')
# #         elif node_type == 'Expression':
# #             color_map.append('lightgray')
# #         elif node_type == 'Shortcut':
# #             color_map.append('khaki')
# #         else:
# #             color_map.append('purple')

# #     plt.figure(figsize=(20, 12))
# #     nx.draw(
# #         G, pos,
# #         with_labels=True,
# #         node_color=color_map,
# #         node_size=3000,
# #         font_size=9,
# #         font_weight='bold',
# #         arrows=True,
# #         edge_color='gray',
# #         arrowstyle='-|>',
# #         linewidths=1
# #     )

# #     filename = os.path.join(output_folder, f"{mapping['mapping_name']}_etl.png")
# #     plt.savefig(filename, bbox_inches='tight')
# #     plt.close()
# #     return filename


# # ver-7

# import os
# import matplotlib.pyplot as plt
# import networkx as nx

# def generate_etl_diagram(mapping, output_folder):
#     G = nx.DiGraph()

#     # Add nodes and label their types
#     for src in mapping['sources']:
#         G.add_node(src['name'], type='Source Definition')

#     for tf in mapping['transformations']:
#         G.add_node(tf['name'], type=tf['type'])

#     for tgt in mapping['targets']:
#         G.add_node(tgt['name'], type='Target Definition')

#     for conn in mapping['connectors']:
#         from_node = conn['from_instance']
#         to_node = conn['to_instance']
#         G.add_edge(from_node, to_node)

#     # Define manual layer ordering (grouped by type, each column)
#     layer_order = [
#         "Lookup Procedure",
#         "Source Definition",
#         "Shortcut",
#         "Application Source Qualifier",
#         "Source Qualifier",
#         "Joiner",
#         "Expression",
#         "Filter",
#         "Router",
#         "Expression_to_Target",
#         "Target Definition"
#     ]

#     # Assign positions in vertical columns (x by layer, y stacked)
#     pos = {}
#     layer_x = {layer: i for i, layer in enumerate(layer_order)}
#     layer_y_tracker = {layer: 0 for layer in layer_order}

#     for node, data in G.nodes(data=True):
#         node_type = data.get('type', 'Expression')

#         # Handle shortcut naming fallback
#         if 'Shortcut' in node and 'Source' in node:
#             node_type = 'Shortcut'
#         elif 'Shortcut' in node and 'Target' in node:
#             node_type = 'Shortcut'

#         x = layer_x.get(node_type, len(layer_order)) * 5
#         y = -layer_y_tracker.get(node_type, 0) * 5
#         pos[node] = (x, y)
#         layer_y_tracker[node_type] += 1

#     # Set node colors
#     color_map = []
#     for node in G:
#         node_type = G.nodes[node].get('type')
#         if node_type == 'Source Definition':
#             color_map.append('skyblue')
#         elif node_type == 'Target Definition':
#             color_map.append('lightgreen')
#         elif node_type == 'Lookup Procedure':
#             color_map.append('plum')
#         elif node_type in ['Application Source Qualifier', 'Source Qualifier']:
#             color_map.append('orange')
#         elif node_type == 'Joiner':
#             color_map.append('gold')
#         elif node_type == 'Filter':
#             color_map.append('red')
#         elif node_type == 'Router':
#             color_map.append('tomato')
#         elif node_type == 'Expression':
#             color_map.append('lightgray')
#         elif node_type == 'Shortcut':
#             color_map.append('khaki')
#         else:
#             color_map.append('white')

#     plt.figure(figsize=(len(layer_order) * 3, max(layer_y_tracker.values()) * 2))
#     nx.draw(
#         G, pos,
#         with_labels=True,
#         node_color=color_map,
#         node_size=3000,
#         font_size=9,
#         font_weight='bold',
#         arrows=True,
#         edge_color='gray',
#         arrowstyle='-|>',
#         linewidths=1
#     )

#     filename = os.path.join(output_folder, f"{mapping['mapping_name']}_etl.png")
#     plt.savefig(filename, bbox_inches='tight')
#     plt.close()
#     return filename


import os
import matplotlib.pyplot as plt
import networkx as nx

def generate_etl_diagram(mapping, output_folder):
    G = nx.DiGraph()

    # Add nodes and label their types
    for src in mapping['sources']:
        G.add_node(src['name'], type='Source Definition')

    for tf in mapping['transformations']:
        G.add_node(tf['name'], type=tf['type'])

    for tgt in mapping['targets']:
        G.add_node(tgt['name'], type='Target Definition')

    for conn in mapping['connectors']:
        from_node = conn['from_instance']
        to_node = conn['to_instance']
        G.add_edge(from_node, to_node)

    # Dynamically determine layer ordering from node types
    all_types = set(data.get('type', 'Expression') for _, data in G.nodes(data=True))
    layer_order = sorted(all_types, key=lambda x: (
        0 if 'Source' in x else
        1 if 'Qualifier' in x else
        2 if x == 'Lookup Procedure' else
        3 if x == 'Joiner' else
        4 if x == 'Expression' else
        5 if x == 'Filter' else
        6 if x == 'Router' else
        7 if 'Target' in x else
        99
    ))

    # Assign positions in vertical columns (x by layer, y stacked)
    pos = {}
    layer_x = {layer: i for i, layer in enumerate(layer_order)}
    layer_y_tracker = {layer: 0 for layer in layer_order}

    for node, data in G.nodes(data=True):
        node_type = data.get('type', 'Expression')

        # Handle shortcut naming fallback
        if 'Shortcut' in node and 'Source' in node:
            node_type = 'Shortcut'
        elif 'Shortcut' in node and 'Target' in node:
            node_type = 'Shortcut'

        x = layer_x.get(node_type, len(layer_order)) * 5
        y = -layer_y_tracker.get(node_type, 0) * 5
        pos[node] = (x, y)
        layer_y_tracker[node_type] += 1

    # Set node colors
    color_palette = {
        'Source Definition': 'skyblue',
        'Target Definition': 'lightgreen',
        'Lookup Procedure': 'plum',
        'Application Source Qualifier': 'orange',
        'Source Qualifier': 'deepskyblue',
        'Joiner': 'gold',
        'Filter': 'red',
        'Router': 'tomato',
        'Expression': 'lightgray',
        'Shortcut': 'khaki'
    }

    color_map = []
    for node in G:
        node_type = G.nodes[node].get('type')
        color_map.append(color_palette.get(node_type, 'purple'))

    plt.figure(figsize=(len(layer_order) * 3, max(layer_y_tracker.values()) * 2))
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=color_map,
        node_size=3000,
        font_size=9,
        font_weight='bold',
        arrows=True,
        edge_color='gray',
        arrowstyle='-|>',
        linewidths=1
    )

    filename = os.path.join(output_folder, f"{mapping['mapping_name']}_etl.png")
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    return filename
