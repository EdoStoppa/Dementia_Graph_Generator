from py2neo import Graph, Node, Relationship, Subgraph


def get_patient_node(graph: Graph, id: str) -> Node:
    q = f"MATCH (p: Patient {{name: '{id}'}}) RETURN p"
    node = graph.evaluate(q)

    return node

def one_to_features(attributes, row, base_node):
    nodes, relationships = [], []
    for attribute in attributes:
        node = Node('Feature', *{attribute: row[attribute]})
        nodes.append(node)
        rel = Relationship(base_node, 'IS', node)
        relationships.append(rel)

    return nodes, relationships

def one_to_features(names, attributes, row, base_node):
    nodes, relationships = [], []
    for name, attribute in zip(names, attributes):
        node = Node('Feature', *{name: row[attribute]})
        nodes.append(node)
        rel = Relationship(base_node, 'IS', node)
        relationships.append(rel)

    return nodes, relationships

def add_new_cat(graph: Graph, father: Node, row, attributes: list, type:str) -> None:
    nodes, rels = [], []

    node_type = Node(type)
    nodes.append(node_type)
    rels.append(Relationship(father, 'SUB_CATEGORY', node_type))

    n, r = one_to_features(attributes, row, node_type)
    nodes += n
    rels += r

    graph.create(Subgraph(nodes, rels))

    return