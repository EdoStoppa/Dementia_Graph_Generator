import pandas as pd
from py2neo import Graph, Node, Relationship, Subgraph
import util as u

def add_general_struct(graph: Graph, discourse: Node, attributes: list, feat_dict: dict) -> None:
    nodes, rels = [], []

    general = Node(*['Category', 'General_Discourse-Based'])
    nodes.append(general)
    rels.append(Relationship(discourse, 'SUB_CATEGORY', general))

    # Create feature nodes and relationships
    n, r = u.one_to_features(attributes, general, feat_dict)
    nodes += n
    rels += r

    graph.create(Subgraph(nodes, rels))

def add_rel_struct(graph: Graph, discourse: Node, attributes: list, feat_dict: dict) -> None:
    nodes, rels = [], []

    relations = Node(*['Category', 'Relations'])
    nodes.append(relations)
    rels.append(Relationship(discourse, 'SUB_CATEGORY', relations))

    attrs = list(zip(attributes[:18], attributes[18:36]))

    for pure, ratio in attrs:
        # Create node for section of basic feature
        new_node = Node(*['Category', pure])
        nodes.append(new_node)

        # Create relation between master node and new subnode
        rels.append(Relationship(relations, 'SUB_CATEGORY', new_node))

        # Create feature nodes and relationships
        n, r = u.one_to_features2(['pure', 'ratio'], [pure, ratio], new_node, feat_dict)
        nodes += n
        rels += r

    # Add last special node
    typ2tok = Node(*['Category', 'Type_2_Token'])
    nodes.append(typ2tok)
    rels.append(Relationship(relations, 'SUB_CATEGORY', typ2tok))

    new_node = Node(*['Feature', attributes[-1]])
    nodes.append(new_node)
    feat_dict[attributes[-1]] = new_node
    rels.append(Relationship(typ2tok, 'IS', new_node))

    graph.create(Subgraph(nodes, rels))

def add_discourse_based(graph: Graph, data_path: str) -> None:
    # Load data into pandas
    data = pd.read_csv(data_path)
    # Get the columns names
    attributes = list(data.columns)[1:]

    # Create a new feature category
    discourse = Node(*['Feature_Type', 'Discourse_Based'])
    graph.create(discourse)

    # Dictionary holding all feature nodes
    feat_dict = {}

    # Add the energy feature structure in the graph
    add_general_struct(graph, discourse, attributes[:3], feat_dict)

    # Add the MFCC feature structure in the graph
    add_rel_struct(graph, discourse, attributes[3:], feat_dict)
    
    rels = []
    for index, row in data.iterrows():
        # Printing progress bar
        u.printProgressBar(index+1, len(data), bar_size=40)
        # Get the patient node
        patient = u.get_patient_node(graph, row['id'])
        if patient is None: continue

        # Add the base relation patient -> feature type
        rels.append(Relationship(patient, 'FEATURE_TYPE', discourse))

        for feat in attributes:
            rels.append(Relationship(patient, 'VALUE', feat_dict[feat], **{'value': float(row[feat])}))

    # Add the feature relationships
    graph.create(Subgraph(relationships=rels))