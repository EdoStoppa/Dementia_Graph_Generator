import pandas as pd
from py2neo import Graph, Node, Relationship, Subgraph
import util as u

def add_anagraphic(graph: Graph, data_path: str) -> None:
    # Load data into pandas
    data = pd.read_csv(data_path)
    # Get the columns names
    attributes = list(data.columns)[1:]

    # Create a new CATEGORY node
    anagraphic = Node(*['Feature_Type', 'Anagraphic'])

    # Dictionary to cache the feature nodes
    feat_dict = {}

    # Generate the features structure
    nodes, relationships = [], []
    for attribute in attributes:
        feat_node = Node(*['Feature', attribute])
        nodes.append(feat_node)
        feat_dict[attribute] = feat_node
        rel = Relationship(anagraphic, 'IS', feat_node)
        relationships.append(rel)

    # Add the relationship that explicit the feature values
    for index, row in data.iterrows():
        # Printing progress bar
        u.printProgressBar(index+1, len(data), bar_size=40)

        # Get the patient node
        patient = u.get_patient_node(graph, row['id'])
        if patient is None: continue

        # Add the base relation patient -> feature type
        relationships.append(Relationship(patient, 'FEATURE_TYPE', anagraphic))
        
        # Create the VALUE relationship between patients and features
        for attribute in attributes:
            feat_node = feat_dict[attribute]
            rel = Relationship(patient, 'VALUE', feat_node, **{'value': float(row[attribute])})
            relationships.append(rel)
        
    # Load to neo4j all the nodes and relationships
    graph.create(Subgraph(nodes + [anagraphic], relationships))