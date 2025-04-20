import networkx as nx

def build_etl_graph(mapping):
    G = nx.DiGraph()
    for conn in mapping['connectors']:
        from_node = conn['from_instance']
        to_node = conn['to_instance']
        if from_node and to_node:
            G.add_edge(from_node, to_node)
    return G

def find_main_workflow_path(G):
    roots = [n for n in G.nodes if G.in_degree(n) == 0]
    longest = []
    for root in roots:
        for path in nx.all_simple_paths(G, source=root, target=None):
            if len(path) > len(longest):
                longest = path
    return longest

def find_branches(G, main_path):
    branches = []
    main_set = set(main_path)
    for node in main_path:
        for neighbor in G.successors(node):
            if neighbor not in main_set:
                branches.append((node, neighbor))
    return branches

def format_main_flow(main_path):
    return ' |->| '.join(f"`{step}`" for step in main_path)

def format_branches(branches):
    lines = []
    for from_node, to_node in branches:
        lines.append(f"{' ' * (main_node_indent(from_node, branches))}|\n{' ' * (main_node_indent(from_node, branches))}v\n`{to_node}`")
    return '\n'.join(lines)

def main_node_indent(node, branches):
    for i, (from_n, _) in enumerate(branches):
        if from_n == node:
            return i * 4 + 2
    return 2

def generate_etl_chain_summary(mapping):
    G = build_etl_graph(mapping)
    main_path = find_main_workflow_path(G)
    branches = find_branches(G, main_path)

    summary = format_main_flow(main_path)
    if branches:
        summary += "\n" + format_branches(branches)

    return summary

def write_etl_chain_summary(mapping, output_folder):
    summary = generate_etl_chain_summary(mapping)
    path = f"{output_folder}/{mapping['mapping_name']}_etl_chain.md"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(summary)
    return path