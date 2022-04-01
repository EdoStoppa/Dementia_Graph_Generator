import pandas as pd
from py2neo import Graph, Node, Relationship, Subgraph
from util import get_patient_node

def add_anagraphic(graph: Graph, data_path: str) -> None:
    # Load data into pandas
    data = pd.read_csv(data_path)
    # Get the columns names
    attributes = list(data.columns)[1:]
    
    for index, row in data.iterrows():
        print(f"    Working on {row['id']}...")
        # Get the patient node
        patient = get_patient_node(graph, row['id'])
        if patient is None: continue
        # Create a new CATEGORY node
        anagraphic = Node('Anagraphic')

        # Add the relationship between patient and category
        graph.create(Relationship(patient, 'BASIC_CATEGORY', anagraphic))
        
        nodes, relationships = [], []
        for attribute in attributes:
            node = Node(attribute, **{'value': row[attribute]})
            nodes.append(node)
            rel = Relationship(anagraphic, 'IS', node)
            relationships.append(rel)
        
        graph.create(Subgraph(nodes, relationships))

    return