from py2neo import Graph, Node, Relationship, Subgraph
import sys

# Simple function to print a completion bar
def printProgressBar(iter, max_iter, bar_size=20, postText=''):
    percentage = iter/max_iter
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'■' * int(bar_size * percentage):{bar_size}s}] {int(100 * percentage)}%  {postText}")
    sys.stdout.flush()

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
def one_to_features(feat_names: list, base_node: Node, feat_dict: dict):
    nodes, relationships = [], []
    for feat_name in feat_names:
        node = Node(*['Feature', feat_name])
        nodes.append(node)
        feat_dict[feat_name] = node
        rel = Relationship(base_node, 'IS', node)
        relationships.append(rel)

    return nodes, relationships

# Given a node, it generate the nodes containing the numerical feature associated
#
# feat_names: Names of all feature after insertion in a node
# feat_data_names: Names of all features inside the dataframe row called "data"
# data: row of a dataframe containing all the numerical features
# base_node: starting node where to attach all the feature nodes
def one_to_features2(feat_names: list, feat_data_names: list, base_node: Node, feat_dict: dict) -> None:
    nodes, relationships = [], []
    for feat_name, feature in zip(feat_names, feat_data_names):
        node = Node(*['Feature', feat_name])
        nodes.append(node)
        feat_dict[feature] = node
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
def add_cat_feat(graph: Graph, father: Node, feat_names: list, sub_name:str, feat_dict: dict) -> None:
    nodes, rels = [], []

    sub = Node(*['Category', sub_name])
    nodes.append(sub)
    rels.append(Relationship(father, 'SUB_CATEGORY', sub))

    n, r = one_to_features(feat_names, sub, feat_dict)
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
def add_sub_category(graph: Graph, father: Node, feat_name_lists: list, cat_name: str, sub_names: list, feat_dict: dict) -> None:
    # Work on the new sub node and sub relation
    sub = Node(*['Category', cat_name])
    sub_rel = Relationship(father, 'SUB_CATEGORY', sub)
    graph.create(Subgraph([sub], [sub_rel]))
    
    # Add all the features
    for sub_name, feat_names in zip(sub_names, feat_name_lists):
        add_cat_feat(graph, sub, feat_names, sub_name, feat_dict)