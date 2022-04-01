from py2neo import Graph, Node, Relationship, Subgraph

# Given a graph and an id, return the node containing the patient associated with the id
#
# graph: Graph containing all patients
# id: identifier associated to a single patient
def get_patient_node(graph: Graph, id: str) -> Node:
    q = f"MATCH (p: Patient {{name: '{id}'}}) RETURN p"
    node = graph.evaluate(q)

    return node

# Given a node, it generate the nodes containing the numerical feature associated
#
# feat_names: Name of all features interested (used both in data retrieval and for naming purpose inside a node)
# data: row of a dataframe containing all the numerical features
# base_node: starting node where to attach all the feature nodes
def one_to_features(feat_names: list, data, base_node: Node):
    nodes, relationships = [], []
    for feat_name in feat_names:
        node = Node(feat_name, **{'value': data[feat_name]})
        nodes.append(node)
        rel = Relationship(base_node, 'IS', node)
        relationships.append(rel)

    return nodes, relationships

# Given a node, it generate the nodes containing the numerical feature associated
#
# feat_names: Names of all feature after insertion in a node
# feat_data_names: Names of all features inside the dataframe row called "data"
# data: row of a dataframe containing all the numerical features
# base_node: starting node where to attach all the feature nodes
def one_to_features2(feat_names: list, feat_data_names: list, data, base_node: Node) -> None:
    nodes, relationships = [], []
    for feat_name, feature in zip(feat_names, feat_data_names):
        node = Node(feat_name, **{'value': data[feature]})
        nodes.append(node)
        rel = Relationship(base_node, 'IS', node)
        relationships.append(rel)

    return nodes, relationships

# Given a father node, this function creates a new subcategory and attach to it all the feature nodes
#
# graph: The graph object used to push on neo4j all the new nodes and relationships
# father: the father node from which the sub-category is born
# data: row of a dataframe containing all numerical features
# feat_names: names of all the features involved
# type: name of the new sub-category
def add_cat_feat(graph: Graph, father: Node, data, feat_names: list, sub_name:str) -> None:
    nodes, rels = [], []

    sub = Node(sub_name)
    nodes.append(sub)
    rels.append(Relationship(father, 'SUB_CATEGORY', sub))

    n, r = one_to_features(feat_names, data, sub)
    nodes += n
    rels += r

    graph.create(Subgraph(nodes, rels))

# Add an higher level sub-category, that will be connected to other sub-categories with features
#
# graph: The graph object containing all nodes and relationships
# father: the father node that will be connected to the sub-category
# data: a dataframe row containing all numerical features
# feat_name_lists: list of lists, each sub-list contains the features that will be connected to a not yet created sub-category
# cat_name: name of the high level sub-category
# sub_names: list of names of all 
def add_sub_category(graph: Graph, father: Node, data, feat_name_lists: list, cat_name: str, sub_names: list) -> None:
    # Work on the new sub node and sub relation
    sub = Node(cat_name)
    sub_rel = Relationship(father, 'SUB_CATEGORY', sub)
    graph.create(Subgraph([sub], [sub_rel]))
    
    # Add all the features
    for sub_name, feat_names in zip(sub_names, feat_name_lists):
        add_cat_feat(graph, sub, data, feat_names, sub_name)